## Description

<!-- Provide a clear and concise description of what this PR does -->

## Related Issues

<!-- Reference related issues (e.g., "Fixes #123", "Closes #456") -->

## Type of Change

<!-- Check all that apply -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test addition/update
- [ ] CI/CD or infrastructure change

## Pre-PR Checklist

<!-- Ensure all items are completed before submitting -->

### Code Quality

- [ ] Code follows existing project style and structure
- [ ] No unnecessary dependencies or debug code left in
- [ ] Removed commented-out code
- [ ] No hardcoded credentials, API keys, or secrets

### Tests

- [ ] All tests pass: `python -m unittest discover`
- [ ] New features have corresponding tests
- [ ] Bug fixes include regression tests
- [ ] Tests run successfully with proper environment setup (FPCALC, env vars)

### Documentation

- [ ] [CHANGELOG.md](CHANGELOG.md) updated in the `[Unreleased]` section for any notable change
- [ ] [README.md](README.md) updated if adding new features or changing behavior
- [ ] Environment variable documentation updated if config changed
- [ ] Added/updated type hints where appropriate

### Git Hygiene

- [ ] Commit messages are concise and clear
- [ ] Prefer small, focused commits (one logical change per commit)
- [ ] No merge conflicts with target branch (`main`)
- [ ] Branch is up to date with `main`
- [ ] No accidental commits (large files, secrets, personal configs)

## Breaking Changes

<!-- If this PR includes breaking changes, describe them here and provide migration instructions -->

- [ ] This PR includes breaking changes
- [ ] Breaking changes are clearly documented below
- [ ] Migration path is provided (if applicable)

### Breaking Changes Description

<!-- Describe breaking changes and how users should migrate -->

## Testing Instructions

<!-- Provide instructions for testing this PR, if applicable -->

### How to Test

1.
2.
3.

### Test Results

<!-- If applicable, include test results or screenshots -->

## Additional Context

<!-- Add any other context, screenshots, or information about the PR here -->

## Checklist for Reviewers

<!-- Maintainers: Check these before merging -->

- [ ] Code follows project conventions and style
- [ ] Logic is sound and well-structured
- [ ] Error handling is appropriate
- [ ] CI tests pass (tests workflow runs successfully)
- [ ] Tests are adequate for the changes
- [ ] API changes are documented (if applicable)
- [ ] Breaking changes are clearly marked and documented
- [ ] All review comments are addressed
- [ ] No unresolved discussions

---

**Note**: Please ensure all items in the Pre-PR Checklist are completed before requesting review. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.
