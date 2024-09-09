# audio-fingerprinter

## Environment Variables

### Development

These environment variables are needed when running the app in development:

- `ENV` (DEV/TEST/PROD)
- `APP_IS_EXPOSED`
- `POOL_INTERNAL_DIR`
- `FLASK_LOGS_ARE_NEEDED`
- `FLASK_LOG_DIR`
- `FLASK_LOG_APP_FILENAME`
- `FLASK_LOG_ERROR_FILENAME`
- `FLASK_LOG_REQUESTS_FILENAME`

### Build

These environment variables are needed when building the container:

- `DOCKERIZED_POOL_DIR`
- `DOCKERIZED_FLASK_LOG_DIR`
- `FLASK_LOG_APP_FILENAME`
- `FLASK_LOG_ERROR_FILENAME`
- `FLASK_LOG_REQUESTS_FILENAME`
- `GUNICORN_LOG_DIR`
- `GUNICORN_LOG_ERROR_FILENAME`
- `GUNICORN_LOG_ACCESS_FILENAME`

### Runtime

These environment variables are needed when running the container:

- `APP_PORT`

## Volumes

- `/app/pool`
- `/var/log/audio-fingerprinter-flask`
- `/var/log/audio-fingerprinter-gunicorn`