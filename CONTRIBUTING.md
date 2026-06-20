# Contributing Guidelines

Thank you for your interest in contributing!
This project is currently maintained by a solo developer, but contributions, suggestions, and improvements are welcome.

## Table of Contents

- [Contributors vs Maintainers](#contributors-vs-maintainers)
  - [Roles Overview](#roles-overview)
  - [Infrastructure & Automation](#infrastructure--automation)
- [Development Workflow](#development-workflow)
  - [0. Fork & Clone](#0-fork--clone)
  - [1. Environment Setup](#1-environment-setup)
  - [2. Branching](#2-branching)
  - [3. Developing](#3-developing)
  - [4. Testing](#4-testing)
  - [5. Committing](#5-committing)
  - [6. Pull Request Process](#6-pull-request-process)
    - [6.1. Pre-PR Checklist](#61-pre-pr-checklist)
    - [6.2. Opening a Pull Request](#62-opening-a-pull-request)
  - [7. Releasing _(For Maintainers)_](#7-releasing-for-maintainers)
- [License & Attribution](#license--attribution)
- [Contact](#contact)

## Contributors vs Maintainers

### Roles Overview

**Contributors**

Anyone can be a contributor by:

- Submitting bug reports or feature requests via GitHub Issues
- Proposing code changes through Pull Requests
- Improving documentation
- Participating in discussions
- Testing and providing feedback

**Maintainers**

The maintainer(s) are responsible for:

- Reviewing and merging Pull Requests
- Managing releases and versioning
- Ensuring code quality and project direction
- Responding to critical issues
- Maintaining the project's infrastructure
- Moving "Unreleased" changelog entries to versioned sections during releases

**Important:** Even maintainers must go through Pull Requests. No direct commits to `main` (or protected branches) are allowed — all changes must be submitted via Pull Requests and go through the standard review process.

_Note: Contributors can submit fixes for critical issues via feature branches. Maintainers may promote these to hotfix branches when urgent production fixes are needed._

### Infrastructure & Automation

**Workflows:**

- **Tests** (`.github/workflows/tests.yaml`): Runs on push and pull requests to `main`
- **Publish** (`.github/workflows/publish.yaml`): Runs only when a tag `v*` is pushed (build/push Docker image)
- **Tests**: Setup Python 3.14, install system dependencies via `scripts/install-dependencies.sh`, run `scripts/setup-filesystem.sh`, then `python -m pytest --cov` (enforces the minimum coverage threshold in `pyproject.toml`)
- **Build / Push to GHCR**: On version tag push, builds the Docker image and pushes it to **`ghcr.io/<GHCR_IMAGE_NAMESPACE>/<AFP_IMAGE_REPO>:<tag>`** using **`GITHUB_TOKEN`**

**Repository automation (maintainer-only):**

- CI uses repository/environment variables and secrets (e.g. `POOL_DIR_INTERNAL`, `FPCALC_INTERNAL_PATH`, `GHCR_IMAGE_NAMESPACE`). Publish uses **`GITHUB_TOKEN`** for **`ghcr.io`** (`packages: write`). Changing workflow behavior or adding secrets is a maintainer responsibility.

**What contributors can do:**

- Open issues and pull requests
- Run tests and CI locally before opening a PR
- Suggest workflow or documentation improvements via PRs or issues

## Development Workflow

We follow [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow): a single long-lived branch (`main`), with short-lived feature branches merged via Pull Requests.

**Workflow steps:** Fork & Clone → Environment Setup → Branching → Developing → Testing → Committing → Pull Request Process → Releasing _(For Maintainers)_

### 0. Fork & Clone

**For contributors:**

1. Fork the repository on GitHub
2. Clone your fork:

   ```bash
   git clone https://github.com/YOUR-USERNAME/audio-fingerprinter.git
   cd audio-fingerprinter
   ```

**For maintainers:**

Clone the main repository directly (replace with the actual repo URL if different):

```bash
git clone https://github.com/BehindTheMusicTree/audio-fingerprinter.git
cd audio-fingerprinter
```

### 1. Environment Setup

Ensure you have:

- **Python 3.14** (matches CI and runtime). **pyenv:** the repo has **`.python-version`** (`3.14.0`). From the project root run **`pyenv install 3.14.0`** (or **`pyenv install -s 3.14.0`** to skip if already present), then **`python --version`** should show 3.14.x when pyenv’s shims are on your `PATH`. Without pyenv, use **`python3.14`** or another way to get 3.14.

- **Virtual environment and Python dependencies:**

  ```bash
  python -m venv .venv
  source .venv/bin/activate   # Linux/macOS
  # .venv\Scripts\activate   # Windows
  pip install -e ".[dev]"
  ```

  **`[dev]`** includes **`bump-my-version`** and **`pytest`**. Prefer **`python -m pytest`** from the repo root (same interpreter as the venv) so **`pyproject.toml`** pytest options apply.

- **System dependencies** (required for fingerprinting and tests):

  - **ffmpeg** — audio decoding (used by pydub)
  - **fpcalc** (Chromaprint) — audio fingerprinting

  **On Ubuntu (CI-like):** Use the project script (requires `sudo`):

  ```bash
  export APP_IS_DOCKERIZED=false
  sudo -E bash scripts/install-dependencies.sh
  ```

  **On macOS:** Install via Homebrew, then use the project’s macOS fpcalc binary:

  ```bash
  brew install ffmpeg chromaprint
  cp env/fpcalc/fpcalc-macos bin/fpcalc
  chmod +x bin/fpcalc
  ```

  Ensure `bin/fpcalc` is on your `PATH` or that the app is configured to use it (see `FPCALC` / config).

- **Environment variables:** Copy `env/.env.example` to `env/.env` and set variables as needed. See [README.md](README.md) for required variables (e.g. `ENV`, `APP_IS_EXPOSED`, `POOL_DIR_INTERNAL`, Flask log settings).

- **Filesystem setup (for tests / local run):** After env is set, run:

  ```bash
  bash scripts/setup-filesystem.sh
  ```

  This creates the pool directory and log paths. It requires `env/calculated_paths/` and `scripts/generate-calculated-paths-env-file.sh` to be run first if your setup uses calculated paths.

### 2. Branching

#### Main branch (`main`)

- The only long-lived branch; always deployable
- All tests must pass before merging
- **No direct commits** — all changes go through Pull Requests
- Releases are tagged from `main`

#### Feature branches (`feature/<name>`)

- One branch per feature or bug fix; branch from `main`
- Include issue numbers when applicable: `feature/123-add-format-support`
- Examples:

  ```bash
  git checkout main && git pull origin main
  git checkout -b feature/improve-error-messages
  git checkout -b feature/45-fix-fpcalc-path
  ```

- Merge into `main` via Pull Request when complete and tested

#### Hotfix branches (`hotfix/<name>`) _(For Maintainers)_

- For urgent production fixes; branch from `main`
- Merge into `main` via Pull Request after review

#### Chore branches (`chore/<name>`)

- For maintenance, CI, docs, or dependency updates; branch from `main`
- Examples: `chore/update-deps`, `chore/ci-python-314`
- Merge into `main` via Pull Request when complete

### 3. Developing

- Follow existing code style (e.g. type hints where used, consistent naming).
- Use the project’s Python and dependency versions; avoid introducing new runtime dependencies without discussion.
- For API or config changes, update [README.md](README.md) and env templates if needed.

### 4. Testing

Tests are run with **pytest** (same as CI), which also collects the existing `unittest.TestCase`-based tests with no changes needed.

**Quick reference:**

```bash
# Activate your venv first
source .venv/bin/activate

# Run all tests with coverage (requires FPCALC and env set; see CI or scripts)
python -m pytest --cov --cov-report=term-missing
# Optional: plain unittest runner (no coverage enforcement)
# python -m unittest discover
```

Do **not** rely on a bare **`pytest`** on `PATH` while `(.venv)` is active: many setups still run **pyenv/Homebrew** `pytest`, so you get **`ModuleNotFoundError: flask`**. Use **`python -m pytest`** (or **`.venv/bin/pytest`**) after **`pip install -e ".[dev]"`**.

- Ensure `FPCALC` points to `bin/fpcalc` (or your system fpcalc).
- CI sets `ENV`, `FPCALC`, `POOL_DIR_INTERNAL`, etc.; replicate those locally if you want CI-like results.
- Test assets live in `test/samples/`; do not commit large or unrelated media files.
- CI enforces a minimum coverage threshold (`[tool.coverage.report]` in `pyproject.toml`); run `python -m pytest --cov --cov-report=term-missing` locally to check for gaps before opening a PR.

### 5. Committing

- Use **concise, clear commit messages** that describe what changed and why.
- Prefer small, focused commits (one logical change per commit).
- **Update [CHANGELOG.md](CHANGELOG.md)** for user-facing changes: add an entry under the `[Unreleased]` section under the appropriate category (Added, Changed, Improved, Fixed, Documentation, etc.). See [CHANGELOG.md](CHANGELOG.md) for format and categories.

### 6. Pull Request Process

#### 6.1. Pre-PR Checklist

Before submitting a Pull Request:

**1. Code & style**

- Code follows existing project style and structure.
- No unnecessary dependencies or debug code left in.

**2. Tests**

- All tests pass locally: `python -m pytest --cov` (also confirms the coverage threshold is met).
- New features or bug fixes include or update tests where appropriate.

**3. Documentation**

- [CHANGELOG.md](CHANGELOG.md) updated in the `[Unreleased]` section for any notable change.
- [README.md](README.md) or env templates updated if you changed config, API, or run instructions.

**4. Git**

- Branch is up to date with `main`.
- No secrets, large binaries, or personal config committed.

#### 6.2. Opening a Pull Request

- **Target branch:** `main`.
- **Title:** Short, imperative summary (e.g. "Add .dockerignore to reduce image size", "Fix fpcalc path in Docker").
- **Description:** A PR template will be automatically provided when opening a PR. Fill it out with:
  - Clear description of what changed and why
  - Related issues (if any)
  - Type of change
  - Complete the Pre-PR Checklist
  - Testing instructions
  - Any additional context
- **CI:** Ensure the CI workflow (tests + Docker build) passes. Fix any failures before requesting review.

### 7. Releasing _(For Maintainers)_

Releases are prepared from the appropriate branch (e.g. `main`). Use the release script (requires `bump-my-version`; install with `pip install -e ".[dev]"`):

```bash
python3 scripts/release.py [patch|minor|major]
# or: ./scripts/release [patch|minor|major]
```

`release.py` is Python — do not run `bash scripts/release.py` (the shell will mis-parse it). Use `python3` or the `scripts/release` shim above.

Default is `patch`. The script will:

1. Move `[Unreleased]` changelog entries into a new versioned section with the current date (ISO).
2. Bump version in `pyproject.toml` via `bump-my-version` (`[tool.bumpversion]` and `[project]` version).
3. Commit the changelog and version changes, create tag `vX.Y.Z`, and push branch and tag.

CI will build and push the Docker image on tag push; ensure `APP_VERSION` (or equivalent) in the workflow matches the release.

## License & Attribution

Contributions are made under the project’s open-source license. You retain authorship of your code; the project retains redistribution rights under the same license.

## Contact

- **Issues** — bug reports, feature requests, or questions: open a [GitHub Issue](https://github.com/BehindTheMusicTree/audio-fingerprinter/issues) (replace with the actual repo URL if different).

Thank you for contributing.
