#!/bin/bash

if [ -z "$APP_PORT" ]; then
    echo "APP_PORT is not set" >&2
    exit 1
fi

exec gunicorn bodzify_api.wsgi:application \
    --bind 0.0.0.0:${APP_PORT} \
    --error-logfile=${GUNICORN_LOG_DIR_SYMLINK_TARGET}${GUNICORN_LOG_ERROR_FILENAME} \
    --access-logfile=${GUNICORN_LOG_DIR_SYMLINK_TARGET}${GUNICORN_LOG_ACCESS_FILENAME} \
    --log-level=info