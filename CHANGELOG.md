# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Changelog Best Practices

### General Principles

- Changelogs are for humans, not machines.
- Include an entry for every version, with the latest first.
- Group similar changes under: Added, Changed, Improved, Deprecated, Removed, Fixed, Documentation, Performance, CI.
- **"Test" is NOT a valid changelog category** - tests should be mentioned within the related feature or fix entry, not as standalone entries.
- Use an "Unreleased" section for upcoming changes.
- Follow Semantic Versioning where possible.
- Use ISO 8601 date format: YYYY-MM-DD.
- Avoid dumping raw git logs; summarize notable changes clearly.

### Guidelines for Contributors

All contributors (including maintainers) should update `CHANGELOG.md` when creating PRs:

1. **Add entries to the `[Unreleased]` section** - Add your changes under the appropriate category (Added, Changed, Improved, Deprecated, Removed, Fixed, Documentation, Performance, CI)
2. **Follow the changelog format** - See examples below for detailed guidelines
3. **Group related changes** - Similar changes should be grouped together
4. **Be descriptive** - Write clear, user-focused descriptions of what changed
5. **Mention tests when relevant** - Tests should be mentioned within the related feature or fix entry, not as standalone entries

**Example:**

```markdown
## [Unreleased]

### Improved

- **Docker image**: Added .dockerignore to exclude dev and test files from build context
```

**Note:** During releases, maintainers will move entries from `[Unreleased]` to a versioned section (e.g., `## [0.2.0] - 2025-01-XX`).

## [Unreleased]

### Changed

- **Packaging**: Runtime and dev dependencies are declared in **`pyproject.toml`** (PEP 621); install with **`pip install .`** or **`pip install -e ".[dev]"`** for release tooling. Removed **`requirements.txt`**, **`requirements-dev.txt`**, and **`setup.py`**. Distribution name is **`audio-fingerprinter`**. Releases use **`bump-my-version`** (`[tool.bumpversion]` in **`pyproject.toml`**); removed **`.bumpversion.cfg`** / **`bump2version`**.
- **CI (Publish)**: Push tag builds to **GitHub Container Registry** — **`ghcr.io/<GHCR_IMAGE_NAMESPACE>/<AFP_IMAGE_REPO>:<ref>`** via **`docker/login-action`** and **`GITHUB_TOKEN`** (`packages: write`). Removes Docker Hub login and **`DOCKERHUB_ACCESS_TOKEN`**; add GitHub variable **`GHCR_IMAGE_NAMESPACE`** (lowercase, same as **BehindTheMusicTree/infrastructure**).

### Fixed

- **CI (Tests)**: `install-dependencies.sh` skips the deadsnakes PPA when `python3.12` is already on `PATH` (from `actions/setup-python`), and the test workflow runs `sudo` with `PATH` preserved so Launchpad connectivity is no longer required for Python on runners.

## [1.4.1] - 2026-03-18

### Improved

- **Settings**: Remove directory existence check for SAMPLE_DIR
- **Releases**: Add a `bump2version`-based release wrapper (`scripts/release.py`) that updates `setup.py`/`.bumpversion.cfg`, moves `[Unreleased]` into a dated section, and creates/pushes version tags

## [1.4.0] - 2026-03-06

### Changed

- **Docker**: Path variables `FLASK_LOG_DIR_EXTERNAL`, `GUNICORN_LOG_DIR`, and pool path are now **runtime-only** (removed from build). The image no longer bakes in default log/pool paths. Operators must pass `-e POOL_DIR_EXTERNAL`, `-e GUNICORN_LOG_DIR`, and `-e FLASK_LOG_DIR_EXTERNAL` (or `*_INTERNAL`) when running the container; entrypoint fails fast with a clear message if any required var is missing. See README.

## [1.3.1] - 2026-03-06

### Fixed

- **Docker**: Image now supports running as arbitrary non-root UID/GID (`--user $(id -u):$(id -g)`). `setup-filesystem.sh` no longer runs `chown`/`chmod` when not root; log dirs can be pointed to `/app/log` (writable by any user). See README for required env overrides (`GUNICORN_LOG_DIR`, `FLASK_LOG_DIR_EXTERNAL`).

## [1.3.0] - 2026-03-06

### Changed

- **Docker**: `POOL_DIR_EXTERNAL` is now a runtime environment variable instead of a build arg, so the same image can be used with different pool paths

## [1.2.4] - 2026-02-21

### Added

- **API**: GET `/health` endpoint for liveness checks (load balancers, monitoring)

## [1.2.3] - 2026-02-03

### Fixed

- **Docker**: Added explicit `apt-get update` before install script to improve network reliability during builds

## [1.2.2] - 2026-02-03

### Added

- **CI**: Added manual trigger (`workflow_dispatch`) to publish workflow for on-demand releases

### Fixed

- **Docker**: Entrypoint now creates log files at runtime for volume-mounted directories, fixing startup errors when log directories are mounted as volumes
- **CI**: Fixed YAML syntax error in tests workflow (`branches: *` → removed branches filter to run on all branches)

## [1.2.0] - 2025-01-29

### Documentation

- **README**: Added comprehensive README with features, table of contents, API documentation, installation, Docker deployment, and usage examples
- **PR template**: Added pull request description template with pre-PR checklist and review guidelines
- **CONTRIBUTING**: Updated to reference PR template in pull request process section

### Fixed

- **CI**: Updated `actions/cache` from deprecated v2 to v4
- **Dependencies**: Removed `python3.12-distutils` from install script (not available in deadsnakes PPA for Ubuntu 22.04; distutils removed in Python 3.12)

## [1.1.0] - 2025-01-29

### Improved

- **Docker image size**: Added `.dockerignore` to exclude `.git`, `test/` (including audio samples), `env/fpcalc/fpcalc-macos`, and dev artifacts from the build context

### Documentation

- **CHANGELOG**: Added CHANGELOG.md with Keep a Changelog format and contributor guidelines
- **CONTRIBUTING**: Added CONTRIBUTING.md with GitHub Flow, environment setup, branching, testing, and PR process
- **Cursor rules**: Added `.cursor/rules/` with focused contributing and changelog practice files; added meta-rule for cursor rules location and format standards

### CI

- **GitHub Flow**: CI runs on `main` only; removed `dev` branch from workflow triggers
- **Workflows**: Renamed CI workflow to `tests.yaml`; added `publish.yaml` (publish runs only on tag push `v*`); tests workflow runs on push/PR to `main`
- **Workflow reuse**: Made tests workflow reusable via `workflow_call`; publish workflow now calls tests workflow instead of duplicating test steps

## [1.0.0] - 2024-09-06

### Added

- Initial release
