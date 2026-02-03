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

### Fixed

- **Docker**: Entrypoint now creates log files at runtime for volume-mounted directories, fixing startup errors when log directories are mounted as volumes

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
