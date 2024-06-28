# Image ubuntu:22.04 used for all fingerprinters env (except dev) for consistent fingerprint generation
FROM ubuntu:22.04

ARG POOL_DIR_SYMLINK_TARGET
ARG LOG_DIR_SYMLINK_TARGET

RUN if [ -z "$POOL_DIR_SYMLINK_TARGET" ]; then echo "The POOL_DIR_SYMLINK_TARGET argument is not provided" >&2; exit 1; fi
RUN if [ -z "$LOG_DIR_SYMLINK_TARGET" ]; then echo "The LOG_DIR_SYMLINK_TARGET argument is not provided" >&2; exit 1; fi

ENV ENV=TEST \
    POOL_DIR_SYMLINK_TARGET=$POOL_DIR_SYMLINK_TARGET \
    LOG_DIR_SYMLINK_TARGET=$LOG_DIR_SYMLINK_TARGET

WORKDIR /app

# software-properties-common is required for add-apt-repository
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y curl jq python3.12 libchromaprint-tools ffmpeg python3.12-distutils && \
    curl https://bootstrap.pypa.io/get-pip.py | python3.12 && \
    rm -rf /var/lib/apt/lists/*

COPY . .

# To run gunicorn as a non-root user without password prompt
# Second apt-get update is necessary to take into account the new repositories from add-apt-repository 
# ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y wget && \
wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.12/gosu-amd64" && \
chmod +x /usr/local/bin/gosu

RUN chmod +x scripts/setup_filesystem.sh

RUN python3.12 -m pip install --no-cache-dir --ignore-installed -r requirements.txt

RUN scripts/setup_filesystem.sh && \
    cp env/fpcalc/fpcalc-ubuntu bin/fpcalc && \
    chmod +x bin/fpcalc