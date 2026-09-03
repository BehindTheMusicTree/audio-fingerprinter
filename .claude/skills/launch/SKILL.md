---
name: launch
description: Use this skill when asked to run, start, or dev-serve audio-fingerprinter, or to confirm a change works against a live instance. Covers Python env setup, filesystem prep, and system dependencies (ffmpeg, fpcalc) this Flask service needs before it will start.
---

# Launch audio-fingerprinter

A standalone Flask REST API (no companion services required to start it —
it's consumed by other repos like hear-the-music-tree-api, but doesn't need
them running itself).

## 1. Python env (first run only)

Requires Python 3.14 (`pyenv install 3.14.0` per `.python-version`):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 2. System dependencies (first run only)

- **macOS**: `brew install ffmpeg chromaprint && cp env/fpcalc/fpcalc-macos bin/fpcalc && chmod +x bin/fpcalc`
- **Linux**: `sudo -E bash scripts/install-dependencies.sh` (set `APP_IS_DOCKERIZED=false` first)

## 3. Env file

Copy `env/.env.example` to `env/.env` and fill in required values (`APP_PORT`
in particular — it has no default, the app won't start without it).

## 4. Filesystem setup

```bash
bash scripts/setup-filesystem.sh
```

## 5. Start the service

```bash
source .venv/bin/activate  # if not already active
python run.py
```

Serves on `0.0.0.0:$APP_PORT`.

## 6. Verify

```bash
curl http://localhost:$APP_PORT/health
```

Expect `{"status": "ok"}`.
