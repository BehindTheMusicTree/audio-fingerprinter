import importlib.util
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest


@pytest.fixture
def release(monkeypatch, tmp_path):
    path = Path(__file__).resolve().parents[1] / "scripts" / "release.py"
    spec = importlib.util.spec_from_file_location("release_preparation", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.REPO_ROOT = tmp_path
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nversion = "1.2.3"\n[tool.bumpversion]\ncurrent_version = "1.2.3"\n'
    )
    monkeypatch.setattr(sys, "argv", ["release.py", "patch"])
    monkeypatch.setattr(module, "current_version_from_changelog", lambda: "1.2.3")
    monkeypatch.setattr(module, "bump_my_version_cmd", lambda: ["bump-my-version"])
    module.update_changelog = Mock()
    module.run = Mock()
    return module


def test_prepares_release_without_git_operations(release):
    release.main()
    release.update_changelog.assert_called_once()
    release.run.assert_called_once_with(
        "bump-my-version", "bump", "patch", "--new-version", "1.2.4", "--allow-dirty"
    )


def test_rejects_version_mismatch_before_modification(release):
    (release.REPO_ROOT / "pyproject.toml").write_text(
        '[project]\nversion = "1.2.2"\n[tool.bumpversion]\ncurrent_version = "1.2.3"\n'
    )
    with pytest.raises(SystemExit, match="Version mismatch"):
        release.main()
    release.update_changelog.assert_not_called()
    release.run.assert_not_called()
