# Image ubuntu:22.04 used for all fingerprinters env (except dev) for consistent fingerprint generation
FROM ubuntu:22.04

ARG FPCALC_INTERNAL_PATH
ARG FLASK_LOG_APP_FILENAME
ARG FLASK_LOG_ERROR_FILENAME
ARG FLASK_LOG_REQUESTS_FILENAME
ARG GUNICORN_LOG_ERROR_FILENAME
ARG GUNICORN_LOG_ACCESS_FILENAME

RUN for var in \
    FPCALC_INTERNAL_PATH \
    FLASK_LOG_APP_FILENAME \
    FLASK_LOG_ERROR_FILENAME \
    FLASK_LOG_REQUESTS_FILENAME \
    GUNICORN_LOG_ERROR_FILENAME \
    GUNICORN_LOG_ACCESS_FILENAME; do \
    if [ -z "$(eval echo \$$var)" ]; then \
        echo "The $var argument is not provided" >&2; \
        exit 1; \
    fi; \
done

ENV APP_IS_DOCKERIZED=true \
    APP_IS_EXPOSED=true \
    ENV=TEST \
    FPCALC=$FPCALC_INTERNAL_PATH \
    FLASK_LOG_APP_FILENAME=$FLASK_LOG_APP_FILENAME \
    FLASK_LOG_ERROR_FILENAME=$FLASK_LOG_ERROR_FILENAME \
    FLASK_LOG_REQUESTS_FILENAME=$FLASK_LOG_REQUESTS_FILENAME \
    GUNICORN_LOG_ERROR_FILENAME=$GUNICORN_LOG_ERROR_FILENAME \
    GUNICORN_LOG_ACCESS_FILENAME=$GUNICORN_LOG_ACCESS_FILENAME

WORKDIR /app

COPY . .

# Writable dirs for non-root. Pass GUNICORN_LOG_DIR and FLASK_LOG_DIR_EXTERNAL at runtime (required).
RUN mkdir -p /app/log/gunicorn /app/log/flask /app/env/calculated_paths && chmod -R 777 /app/log /app/env/calculated_paths

RUN apt-get update && \
    bash scripts/install-dependencies.sh && \
    python3.12 -m pip install --no-cache-dir --ignore-installed . && \
    chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
