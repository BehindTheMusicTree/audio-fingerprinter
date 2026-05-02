"""Fail fast if pytest is not using an environment with the project installed."""

import importlib.util
import sys

import pytest

if importlib.util.find_spec("flask") is None:
    pytest.exit(
        "Flask not found — this interpreter does not have the project dependencies.\n"
        f"  sys.executable = {sys.executable}\n"
        "  Fix: activate .venv, run: pip install -e .  (or pip install -e \".[dev]\")\n"
        "  Use:  python -m pytest  (not a bare `pytest` on PATH from pyenv/Homebrew).",
        returncode=1,
    )
