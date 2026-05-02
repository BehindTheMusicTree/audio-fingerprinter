#!/usr/bin/env python3
"""Release wrapper: bump version with bump-my-version, update CHANGELOG, commit, tag, push."""

import importlib.metadata
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = REPO_ROOT / "CHANGELOG.md"


def bump_my_version_cmd() -> list[str]:
    """Resolve bump-my-version: venv script, PATH, or same-interpreter ``python -m bumpversion``."""
    for rel in (
        ".venv/bin/bump-my-version",
        ".venv/Scripts/bump-my-version.exe",
    ):
        path = REPO_ROOT / rel
        if path.is_file():
            return [str(path)]
    found = shutil.which("bump-my-version")
    if found:
        return [found]
    try:
        importlib.metadata.version("bump-my-version")
    except importlib.metadata.PackageNotFoundError:
        sys.exit(
            "bump-my-version is not installed for this Python.\n"
            f"  Install dev deps: {sys.executable} -m pip install -e '.[dev]'\n"
            "Or activate a .venv where you ran pip install -e '.[dev]'."
        )
    return [sys.executable, "-m", "bumpversion"]


def current_version_from_changelog() -> str | None:
    """Latest released version: first ## [X.Y.Z] after the last [Unreleased]."""
    text = CHANGELOG.read_text()
    idx = text.rfind("## [Unreleased]")
    if idx == -1:
        return None
    m = re.search(r"## \[(\d+\.\d+\.\d+)\]", text[idx:])
    return m.group(1) if m else None


def unreleased_content(text: str) -> tuple[str, str, str] | None:
    """Returns (before, unreleased_block, after) or None. Uses last [Unreleased] (release history)."""
    idx = text.rfind("## [Unreleased]")
    if idx == -1:
        return None
    tail = text[idx:]
    m = re.match(r"## \[Unreleased\]\s*\n(.*?)(\n\n## \[\d+\.\d+\.\d+\].*)", tail, re.DOTALL)
    if not m:
        return None
    return text[:idx], m.group(1).rstrip(), m.group(2)


def bump(version: str, part: str) -> str:
    major, minor, patch = (int(x) for x in version.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"part must be major|minor|patch, got {part!r}")


def update_changelog(new_version: str, today: str) -> None:
    text = CHANGELOG.read_text()
    parts = unreleased_content(text)
    if not parts:
        sys.exit("CHANGELOG: could not find [Unreleased] block followed by version section")
    before, unreleased_block, after = parts
    new_section = f"## [Unreleased]\n\n## [{new_version}] - {today}\n\n{unreleased_block}"
    CHANGELOG.write_text(before + new_section + after)


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=REPO_ROOT, check=check, text=True)


def main() -> None:
    part = (sys.argv[1] if len(sys.argv) > 1 else "patch").lower()
    if part not in ("major", "minor", "patch"):
        sys.exit("Usage: release.py [patch|minor|major]  (default: patch)")

    current = current_version_from_changelog()
    if not current:
        sys.exit("CHANGELOG: no versioned section found after [Unreleased]")
    new_version = bump(current, part)
    today = date.today().isoformat()

    update_changelog(new_version, today)
    run(*bump_my_version_cmd(), "bump", part, "--new-version", new_version, "--allow-dirty")
    run("git", "add", "CHANGELOG.md", "pyproject.toml")
    run("git", "commit", "-m", f"Release {new_version}")
    run("git", "tag", f"v{new_version}")
    run("git", "push", "origin", "HEAD")
    run("git", "push", "origin", f"v{new_version}")
    print(f"Released {new_version} (tag v{new_version})")


if __name__ == "__main__":
    main()
