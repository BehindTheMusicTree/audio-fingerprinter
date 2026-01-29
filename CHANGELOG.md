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

- **Docker image**: Switched base to python:3.12-slim and added .dockerignore
  - Excludes .git, test samples, and dev files from build context

### Documentation

- **CHANGELOG**: Added CHANGELOG.md with Keep a Changelog format and contributor guidelines.
```

**Note:** During releases, maintainers will move entries from `[Unreleased]` to a versioned section (e.g., `## [0.2.0] - 2025-01-XX`).

## [Unreleased]

### Improved

- **Docker image size**: Reduced image size by excluding unnecessary files and using a slimmer base
  - Added `.dockerignore` to exclude `.git`, `test/` (including audio samples), `env/fpcalc/fpcalc-macos`, and dev artifacts from the build context
  - Switched base image from `ubuntu:22.04` to `python:3.12-slim` to avoid PPA and extra system packages
  - Install only runtime apt dependencies (`ffmpeg`, `libchromaprint-tools`) with `--no-install-recommends` and clean apt cache in the same layer

### Documentation

- **CHANGELOG**: Added CHANGELOG.md with Keep a Changelog format and contributor guidelines.

## [0.1.0] - 2025-01-29

### Added

- **Flask API**: Audio fingerprinting service with POST `/fingerprint-audio` endpoint
  - Accepts filename in pool directory and returns duration and base64-encoded fingerprint
  - Uses pyacoustid and fpcalc (Chromaprint), pydub for format validation
- **Pool directory**: Configurable audio pool path (`AUDIO_FINGERPRINT_POOL_DIR_ABS_PATH`) for files to fingerprint
- **Docker**: Dockerfile for containerized deployment with fpcalc (Ubuntu) and Flask
- **Config**: Environment-based config (DEV, TEST, GITHUB_CI_TEST, PROD) and dotenv support
- **Errors**: Structured error responses for file not found, wrong file type, and fpcalc status 2

### CI

- **CI workflow**: GitHub Actions workflow for tests (see `.github/workflows/CI.yaml`)
