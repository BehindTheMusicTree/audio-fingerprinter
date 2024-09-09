# audio-fingerprinter

## Environment Variables

### Development

These environment variables are needed when running the app in development:

- `ENV`: 
- `APP_IS_EXPOSED`: Whether the app is exposed (true/false)
- `POOL_INTERNAL_DIR`: Internal directory for the pool
- `FLASK_LOGS_ARE_NEEDED`: Whether Flask logs are needed (true/false)
- `FLASK_LOG_DIR`: Directory for Flask logs
- `FLASK_LOG_APP_FILENAME`: Filename for Flask app log
- `FLASK_LOG_ERROR_FILENAME`: Filename for Flask error log
- `FLASK_LOG_REQUESTS_FILENAME`: Filename for Flask requests log
- `GUNICORN_LOG_DIR`: Directory for Gunicorn logs
- `GUNICORN_LOG_ACCESS_FILENAME`: Filename for Gunicorn access log
- `GUNICORN_LOG_ERROR_FILENAME`: Filename for Gunicorn error log

### Build

These environment variables are needed when building the container:

- `APP_IS_EXPOSED`: Whether the app is exposed (true/false)
- `POOL_DIR_SYMLINK_TARGET`: Target directory for pool symlink
- `FLASK_LOG_DIR_SYMLINK_TARGET`: Target directory for Flask log symlink
- `GUNICORN_LOG_DIR_SYMLINK_TARGET`: Target directory for Gunicorn log symlink

### Runtime

These environment variables are needed when running the container:

- `AUDIO_FINGERPRINTER_PORT`: Port on which the audio fingerprinter service runs

## Volumes

- `/app/pool`: Directory for pool data
- `/var/log/flask`: Directory for Flask logs
- `/var/log/gunicorn`: Directory for Gunicorn logs