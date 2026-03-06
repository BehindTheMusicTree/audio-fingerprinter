# Audio Fingerprinter Flask

A Flask-based REST API service for generating audio fingerprints using Chromaprint. This service accepts audio files from a pool directory and returns their acoustic fingerprints and duration, enabling audio identification and matching capabilities.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Request Format](#request-format)
  - [Response Format](#response-format)
  - [Error Handling](#error-handling)
- [Development](#development)
- [Docker Deployment](#docker-deployment)
- [Environment Variables](#environment-variables)
- [Volumes](#volumes)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Audio Fingerprinting**: Generate acoustic fingerprints using Chromaprint (fpcalc) for audio identification
- **Multiple Format Support**: Supports common audio formats including MP3, WAV, and FLAC
- **REST API**: Simple HTTP POST endpoint for fingerprint generation
- **File Validation**: Validates audio file types before processing
- **Error Handling**: Structured error responses with specific error codes
- **Logging**: Comprehensive logging with rotating file handlers for app, error, and request logs
- **Docker Support**: Containerized deployment with Gunicorn for production
- **Environment-based Configuration**: Support for DEV, TEST, and PROD environments
- **Base64 Encoding**: Returns fingerprints as base64-encoded strings for easy transmission

## Requirements

- Python 3.12
- ffmpeg (for audio decoding via pydub)
- fpcalc (Chromaprint) - included in `bin/` directory
- System dependencies: `libchromaprint-tools`, `ffmpeg`

## Installation

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/BehindTheMusicTree/bodzify-audio-fingerprinter-flask.git
   cd bodzify-audio-fingerprinter-flask
   ```

2. Create a virtual environment:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate   # Windows
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install system dependencies:
   - **Ubuntu/Linux**: Run `sudo -E bash scripts/install-dependencies.sh` (set `APP_IS_DOCKERIZED=false`)
   - **macOS**: `brew install ffmpeg chromaprint && cp env/fpcalc/fpcalc-macos bin/fpcalc && chmod +x bin/fpcalc`

5. Set up environment variables (see [Configuration](#configuration))

6. Set up filesystem:
   ```bash
   bash scripts/setup-filesystem.sh
   ```

## Configuration

Copy `env/.env.dev_template` to `env/.env` and configure the required environment variables. See [Environment Variables](#environment-variables) section for details.

## Usage

### API Endpoints

#### GET `/health`

Liveness check for load balancers and monitoring. Returns 200 when the service is up.

**Response (200):**
```json
{
  "status": "ok"
}
```

#### POST `/fingerprint-audio`

Generates an audio fingerprint for a file in the pool directory.

**Request Format:**

```json
{
  "filename": "example.mp3",
  "title": "Example Song Title",      // Optional
  "userId": "user123"                  // Optional
}
```

**Response Format:**

Success (200):
```json
{
  "duration": 245.5,
  "fingerprint": "AQAA...",
  "fileBytesNum": 5242880
}
```

Error (400/422/500):
```json
{
  "status": 400,
  "message": "Error message"
}
```

### Error Handling

The API returns structured error responses:

- **400 Bad Request**: Invalid file type, file not found in pool, or missing filename
- **422 Unprocessable Entity**: fpcalc status 2 (file may be corrupted or too short)
- **500 Internal Server Error**: Unexpected errors during processing

Error codes:
- `Audio Fingerprinter Error Code 1`: fpcalc exited with status 2
- `Audio Fingerprinter Error Code 2`: Wrong file extension
- `Audio Fingerprinter Error Code 3`: Wrong file type (not a valid audio file)
- `Audio Fingerprinter Error Code 4`: File not found in pool directory

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow, testing, and contribution guidelines.

### Running Locally

```bash
python run.py
```

The service will start on `0.0.0.0:PORT` (configured via `APP_PORT` environment variable).

## Docker Deployment

### Build

Build the Docker image with required build arguments:

```bash
docker build \
  --build-arg FPCALC_INTERNAL_PATH=/app/bin/fpcalc \
  --build-arg FLASK_LOG_DIR_EXTERNAL=/var/log/audio-fingerprinter-flask \
  --build-arg FLASK_LOG_APP_FILENAME=app.log \
  --build-arg FLASK_LOG_ERROR_FILENAME=error.log \
  --build-arg FLASK_LOG_REQUESTS_FILENAME=requests.log \
  --build-arg GUNICORN_LOG_DIR=/var/log/audio-fingerprinter-gunicorn \
  --build-arg GUNICORN_LOG_ERROR_FILENAME=error.log \
  --build-arg GUNICORN_LOG_ACCESS_FILENAME=access.log \
  -t audio-fingerprinter:latest .
```

### Run

```bash
docker run -d \
  -p 5000:5000 \
  -v /path/to/pool:/app/pool \
  -v /path/to/logs:/var/log/audio-fingerprinter-flask \
  -v /path/to/gunicorn-logs:/var/log/audio-fingerprinter-gunicorn \
  -e POOL_DIR_EXTERNAL=/app/pool \
  -e APP_PORT=5000 \
  audio-fingerprinter:latest
```

## Environment Variables

### Development

These environment variables are needed when running the app in development:

- `ENV` (DEV/TEST/PROD)
- `APP_IS_EXPOSED`
- `POOL_DIR_INTERNAL`
- `FLASK_LOG_DIR_INTERNAL` or `FLASK_LOG_DIR_EXTERNAL`
- `FLASK_LOG_APP_FILENAME`
- `FLASK_LOG_ERROR_FILENAME`
- `FLASK_LOG_REQUESTS_FILENAME`

### Build

These environment variables are needed when building the container:

- `FLASK_LOG_DIR_EXTERNAL`
- `FLASK_LOG_APP_FILENAME`
- `FLASK_LOG_ERROR_FILENAME`
- `FLASK_LOG_REQUESTS_FILENAME`
- `GUNICORN_LOG_DIR`
- `GUNICORN_LOG_ERROR_FILENAME`
- `GUNICORN_LOG_ACCESS_FILENAME`

### Runtime

These environment variables are needed when running the container:

- `POOL_DIR_EXTERNAL` – path to the pool directory inside the container (e.g. `/app/pool` when using the volume mount above)
- `APP_PORT`

## Volumes

- `/app/pool` - Audio files pool directory
- `/var/log/audio-fingerprinter-flask` - Flask application logs
- `/var/log/audio-fingerprinter-gunicorn` - Gunicorn server logs

## Testing

Run tests with:

```bash
python -m unittest discover
```

Tests require:
- `FPCALC` environment variable pointing to fpcalc binary
- Proper environment configuration (see test setup)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development workflow (GitHub Flow)
- Branching strategy
- Testing requirements
- Commit message guidelines
- Pull request process

## License

[Add license information here]
