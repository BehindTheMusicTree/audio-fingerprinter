#!/bin/bash

echo "Starting entrypoint script"

if [ -z "$APP_PORT" ]; then
    echo "APP_PORT is not set" >&2
    exit 1
fi

echo "APP_PORT: $APP_PORT"
echo "GUNICORN_LOG_DIR: $GUNICORN_LOG_DIR"
echo "GUNICORN_LOG_ERROR_FILENAME: $GUNICORN_LOG_ERROR_FILENAME"
echo "GUNICORN_LOG_ACCESS_FILENAME: $GUNICORN_LOG_ACCESS_FILENAME"

exec gunicorn audio_fingerprinter.wsgi:application \
    --bind 0.0.0.0:${APP_PORT} \
    --error-logfile=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ERROR_FILENAME} \
    --access-logfile=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ACCESS_FILENAME} \
    --log-level=debug \
    --capture-output \
    --log-file=-