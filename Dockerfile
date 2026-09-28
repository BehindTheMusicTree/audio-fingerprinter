# Official Python on Debian Bookworm — avoids deadsnakes/PPA during build (Launchpad can be unreachable).
# If you relied on Ubuntu 22.04 + pinned ffmpeg for byte-identical fingerprints, re-validate after this change.
FROM python:3.14-slim-bookworm

# Log filenames are required at runtime (settings.py / scripts/setup-filesystem.sh fail fast), so one
# prebuilt image serves every environment. FPCALC is baked in: the image itself places the binary there.
ENV APP_IS_DOCKERIZED=true \
    APP_IS_EXPOSED=true \
    ENV=TEST \
    FPCALC=/app/bin/fpcalc

WORKDIR /app

COPY . .

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ffmpeg \
        libchromaprint-tools \
        tzdata \
        curl \
        jq \
        ca-certificates \
        wget \
    && wget -qO /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.12/gosu-amd64" \
    && chmod +x /usr/local/bin/gosu \
    && rm -rf /var/lib/apt/lists/*

# Writable dirs for non-root. Pass GUNICORN_LOG_DIR and FLASK_LOG_DIR_EXTERNAL at runtime (required).
RUN mkdir -p /app/log/gunicorn /app/log/flask /app/env/calculated_paths && chmod -R 777 /app/log /app/env/calculated_paths

RUN cp env/fpcalc/fpcalc-ubuntu bin/fpcalc && chmod +x bin/fpcalc

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir --ignore-installed . \
    && chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
