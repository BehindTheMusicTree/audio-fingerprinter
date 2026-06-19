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

- Python 3.14
- ffmpeg (for audio decoding via pydub)
- fpcalc (Chromaprint) - included in `bin/` directory
- System dependencies: `libchromaprint-tools`, `ffmpeg`

## Installation

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/BehindTheMusicTree/audio-fingerprinter.git
   cd audio-fingerprinter
   ```

2. Create a virtual environment (Python **3.14**; **pyenv:** **`pyenv install 3.14.0`** per **`.python-version`**, then **`python -m venv .venv`**):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate   # Windows
   ```

3. Install Python dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
   **`[dev]`** adds **`bump-my-version`** and **`pytest`**. If you use **pytest**, run **`python -m pytest`** from the repo root so **`pyproject.toml`** (`testpaths`, `pythonpath`) applies. Runtime-only install: **`pip install .`**

4. Install system dependencies:
   - **Ubuntu/Linux**: Run `sudo -E bash scripts/install-dependencies.sh` (set `APP_IS_DOCKERIZED=false`)
   - **macOS**: `brew install ffmpeg chromaprint && cp env/fpcalc/fpcalc-macos bin/fpcalc && chmod +x bin/fpcalc`

5. Set up environment variables (see [Configuration](#configuration))

6. Set up filesystem:
   ```bash
   bash scripts/setup-filesystem.sh
   ```

## Configuration

Copy `env/.env.example` to `env/.env` and configure the required environment variables. See [Environment Variables](#environment-variables) section for details.

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

**CI:** Coolify builds and deploys the image directly from this git repository — there is no GitHub Actions publish workflow or GHCR image.

### Build

Build the Docker image with required build arguments (path vars are not build args; they are required at runtime):

```bash
docker build \
  --build-arg FPCALC_INTERNAL_PATH=/app/bin/fpcalc \
  --build-arg FLASK_LOG_APP_FILENAME=app.log \
  --build-arg FLASK_LOG_ERROR_FILENAME=error.log \
  --build-arg FLASK_LOG_REQUESTS_FILENAME=requests.log \
  --build-arg GUNICORN_LOG_ERROR_FILENAME=error.log \
  --build-arg GUNICORN_LOG_ACCESS_FILENAME=access.log \
  -t audio-fingerprinter:latest .
```

### Run

Path variables are **required at runtime** (not baked into the image). Pass them with `-e` in every environment:

```bash
docker run -d \
  -p 5000:5000 \
  -v /path/to/pool:/app/pool \
  -v /path/to/logs:/var/log/audio-fingerprinter-flask \
  -v /path/to/gunicorn-logs:/var/log/audio-fingerprinter-gunicorn \
  -e POOL_DIR_EXTERNAL=/app/pool \
  -e APP_PORT=5000 \
  -e GUNICORN_LOG_DIR=/var/log/audio-fingerprinter-gunicorn \
  -e FLASK_LOG_DIR_EXTERNAL=/var/log/audio-fingerprinter-flask \
  audio-fingerprinter:latest
```

### Run as non-root (e.g. CI with shared pool volume)

To avoid permission issues when the host and container share the pool directory, run with `--user "$(id -u):$(id -g)"`. Point log dirs to the image’s writable `/app/log` and use a non-privileged port (e.g. 3002). All path vars are required at runtime:

```bash
docker run -d \
  --user "$(id -u):$(id -g)" \
  -v /path/to/pool:$AFP_POOL_DIR_EXTERNAL \
  -p 3002:3002 \
  -e POOL_DIR_EXTERNAL=$AFP_POOL_DIR_EXTERNAL \
  -e APP_PORT=3002 \
  -e GUNICORN_LOG_DIR=/app/log/gunicorn/ \
  -e FLASK_LOG_DIR_EXTERNAL=/app/log/flask \
  audio-fingerprinter:latest
```

Logs will be under `/app/log` inside the container (gunicorn and flask subdirs). Omit `-v` for log dirs; the image provides writable `/app/log` for the process user.

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

These environment variables are needed when building the container (path dirs are not build args):

- `FPCALC_INTERNAL_PATH`
- `FLASK_LOG_APP_FILENAME`
- `FLASK_LOG_ERROR_FILENAME`
- `FLASK_LOG_REQUESTS_FILENAME`
- `GUNICORN_LOG_ERROR_FILENAME`
- `GUNICORN_LOG_ACCESS_FILENAME`

### Runtime (required)

These must be set when running the container (fail fast if missing):

- `POOL_DIR_EXTERNAL` or `POOL_DIR_INTERNAL` – pool directory path inside the container
- `APP_PORT` – port the app binds to
- `GUNICORN_LOG_DIR` – when `APP_IS_EXPOSED=true` (default in image)
- `FLASK_LOG_DIR_EXTERNAL` or `FLASK_LOG_DIR_INTERNAL` – Flask log directory

When running with `--user` (non-root), use writable paths: `GUNICORN_LOG_DIR=/app/log/gunicorn/`, `FLASK_LOG_DIR_EXTERNAL=/app/log/flask`.

## Volumes

Mount paths are defined by runtime env; the image does not bake in default log or pool paths.

- Pool: mount where `POOL_DIR_EXTERNAL` points (e.g. `/app/pool`)
- Flask logs: mount where `FLASK_LOG_DIR_EXTERNAL` points (e.g. `/var/log/...` or `/app/log/flask` for non-root)
- Gunicorn logs: mount where `GUNICORN_LOG_DIR` points (e.g. `/var/log/...` or `/app/log/gunicorn/` for non-root)

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
