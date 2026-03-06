#!/bin/bash

echo "Starting entrypoint script"

if [ -z "$APP_PORT" ]; then
    echo "APP_PORT must be set at runtime" >&2
    exit 1
fi

if [ -z "$POOL_DIR_EXTERNAL" ] && [ -z "$POOL_DIR_INTERNAL" ]; then
    echo "POOL_DIR_EXTERNAL or POOL_DIR_INTERNAL must be set at runtime" >&2
    exit 1
fi

if [ -z "$FLASK_LOG_DIR_EXTERNAL" ] && [ -z "$FLASK_LOG_DIR_INTERNAL" ]; then
    echo "FLASK_LOG_DIR_EXTERNAL or FLASK_LOG_DIR_INTERNAL must be set at runtime" >&2
    exit 1
fi

if [ "$APP_IS_EXPOSED" = "true" ] && [ -z "$GUNICORN_LOG_DIR" ]; then
    echo "GUNICORN_LOG_DIR must be set at runtime when APP_IS_EXPOSED=true" >&2
    exit 1
fi

echo "APP_PORT: $APP_PORT"
echo "GUNICORN_LOG_DIR: $GUNICORN_LOG_DIR"
echo "GUNICORN_LOG_ERROR_FILENAME: $GUNICORN_LOG_ERROR_FILENAME"
echo "GUNICORN_LOG_ACCESS_FILENAME: $GUNICORN_LOG_ACCESS_FILENAME"

cd /app

echo "Setting up filesystem (creating log files in mounted volumes)..."
bash scripts/setup-filesystem.sh || { echo "setup-filesystem.sh failed" >&2; exit 1; }

exec gunicorn wsgi:application \
    --bind 0.0.0.0:${APP_PORT} \
    --chdir /app \
    --error-logfile=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ERROR_FILENAME} \
    --access-logfile=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ACCESS_FILENAME} \
    --log-level=debug \
    --capture-output \
    --log-file=-