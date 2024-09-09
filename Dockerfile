# Image ubuntu:22.04 used for all fingerprinters env (except dev) for consistent fingerprint generation
FROM ubuntu:22.04

ARG APP_IS_EXPOSED
ARG POOL_DIR
ARG FLASK_LOGS_ARE_NEEDED
ARG FLASK_LOG_DIR
ARG FLASK_LOG_APP_FILENAME
ARG FLASK_LOG_ERROR_FILENAME
ARG FLASK_LOG_REQUESTS_FILENAME
ARG GUNICORN_LOG_DIR
ARG GUNICORN_LOG_ERROR_FILENAME
ARG GUNICORN_LOG_ACCESS_FILENAME


RUN for var in \
    APP_IS_EXPOSED \
    POOL_DIR \
    FLASK_LOGS_ARE_NEEDED \
    FLASK_LOG_DIR \
    FLASK_LOG_APP_FILENAME \
    FLASK_LOG_ERROR_FILENAME \
    FLASK_LOG_REQUESTS_FILENAME \
    GUNICORN_LOG_DIR \
    GUNICORN_LOG_ERROR_FILENAME \
    GUNICORN_LOG_ACCESS_FILENAME; do \
    if [ -z "$(eval echo \$$var)" ]; then \
        echo "The $var argument is not provided" >&2; \
        exit 1; \
    fi; \
done

ENV APP_IS_DOCKERIZED=true \
    ENV=TEST \
    APP_IS_EXPOSED=$APP_IS_EXPOSED \
    POOL_DIR=$POOL_DIR \
    FLASK_LOGS_ARE_NEEDED=$FLASK_LOGS_ARE_NEEDED \
    FLASK_LOG_DIR=$FLASK_LOG_DIR \
    FLASK_LOG_APP_FILENAME=$FLASK_LOG_APP_FILENAME \
    FLASK_LOG_ERROR_FILENAME=$FLASK_LOG_ERROR_FILENAME \
    FLASK_LOG_REQUESTS_FILENAME=$FLASK_LOG_REQUESTS_FILENAME \
    GUNICORN_LOG_DIR=$GUNICORN_LOG_DIR \
    GUNICORN_LOG_ERROR_FILENAME=$GUNICORN_LOG_ERROR_FILENAME \
    GUNICORN_LOG_ACCESS_FILENAME=$GUNICORN_LOG_ACCESS_FILENAME

WORKDIR /app

COPY . .
RUN chmod +x scripts/setup_filesystem.sh && \
    bash scripts/setup_filesystem.sh && \
    bash scripts/install_dependencies.sh && \
    python3.12 -m pip install --no-cache-dir --ignore-installed -r requirements.txt && \
    chmod +x entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]