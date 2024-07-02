# Image ubuntu:22.04 used for all fingerprinters env (except dev) for consistent fingerprint generation
FROM ubuntu:22.04

ARG APP_IS_EXPOSED
ARG POOL_DIR_SYMLINK_TARGET
ARG FLASK_LOG_DIR_SYMLINK_TARGET
ARG GUNICORN_LOG_DIR_SYMLINK_TARGET
ARG POOL_INTERNAL_DIR
ARG FLASK_LOGS_ARE_NEEDED
ARG FLASK_LOG_DIR
ARG FLASK_LOG_APP_FILENAME
ARG FLASK_LOG_ERROR_FILENAME
ARG FLASK_LOG_REQUESTS_FILENAME

RUN if [ -z "$APP_IS_EXPOSED" ]; then echo "The APP_IS_EXPOSED argument is not provided" >&2; exit 1; fi
RUN if [ -z "$POOL_DIR_SYMLINK_TARGET" ]; then echo "The POOL_DIR_SYMLINK_TARGET argument is not provided" >&2; exit 1; fi
RUN if [ -z "$FLASK_LOG_DIR_SYMLINK_TARGET" ]; then echo "The FLASK_LOG_DIR_SYMLINK_TARGET argument is not provided" >&2; exit 1; fi
RUN if [ -z "$GUNICORN_LOG_DIR_SYMLINK_TARGET" ]; then echo "The GUNICORN_LOG_DIR_SYMLINK_TARGET argument is not provided" >&2; exit 1; fi
RUN if [ -z "$POOL_INTERNAL_DIR" ]; then echo "The POOL_INTERNAL_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$FLASK_LOGS_ARE_NEEDED" ]; then echo "The FLASK_LOGS_ARE_NEEDED argument is not provided" >&2; exit 1; fi
RUN if [ -z "$FLASK_LOG_DIR" ]; then echo "The FLASK_LOG_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$FLASK_LOG_APP_FILENAME" ]; then echo "The FLASK_LOG_APP_FILENAME argument is not provided" >&2; exit 1; fi
RUN if [ -z "$FLASK_LOG_ERROR_FILENAME" ]; then echo "The FLASK_LOG_ERROR_FILENAME argument is not provided" >&2; exit 1; fi
RUN if [ -z "$FLASK_LOG_REQUESTS_FILENAME" ]; then echo "The FLASK_LOG_REQUESTS_FILENAME argument is not provided" >&2; exit 1; fi

ENV APP_IS_DOCKERIZED=true \
    ENV=TEST \
    APP_IS_EXPOSED=$APP_IS_EXPOSED \
    POOL_DIR_SYMLINK_TARGET=$POOL_DIR_SYMLINK_TARGET \
    FLASK_LOG_DIR_SYMLINK_TARGET=$FLASK_LOG_DIR_SYMLINK_TARGET \
    GUNICORN_LOG_DIR_SYMLINK_TARGET=$GUNICORN_LOG_DIR_SYMLINK_TARGET \
    POOL_INTERNAL_DIR=$POOL_INTERNAL_DIR \
    FLASK_LOGS_ARE_NEEDED=$FLASK_LOGS_ARE_NEEDED \
    FLASK_LOG_DIR=$FLASK_LOG_DIR \
    FLASK_LOG_APP_FILENAME=$FLASK_LOG_APP_FILENAME \
    FLASK_LOG_ERROR_FILENAME=$FLASK_LOG_ERROR_FILENAME \
    FLASK_LOG_REQUESTS_FILENAME=$FLASK_LOG_REQUESTS_FILENAME

WORKDIR /app

COPY . .
RUN chmod +x scripts/setup_filesystem.sh
RUN bash scripts/install_dependencies.sh
RUN python3.12 -m pip install --no-cache-dir --ignore-installed -r requirements.txt