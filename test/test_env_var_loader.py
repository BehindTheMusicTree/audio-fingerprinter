#!/usr/bin/env python

import subprocess
from unittest.mock import patch

import pytest

from audio_fingerprinter.env_var_loader import (
    load_calculated_env_paths,
    load_env_vars_from_file_if_exists,
    load_required_bool_env_var,
    load_required_int_env_var,
    load_required_path_env_var,
    load_required_secret_env_var,
    load_required_str_env_var,
)

VAR_NAME = 'SOME_ENV_VAR'


def test_load_required_str_env_var_returns_value(monkeypatch):
    monkeypatch.setenv(VAR_NAME, 'some-value')
    assert load_required_str_env_var(VAR_NAME) == 'some-value'


def test_load_required_str_env_var_must_print_value_false(monkeypatch, capsys):
    monkeypatch.setenv(VAR_NAME, 'secret-value')
    load_required_str_env_var(VAR_NAME, must_print_value=False)
    assert 'secret-value' not in capsys.readouterr().out


def test_load_required_str_env_var_missing_raises(monkeypatch):
    monkeypatch.delenv(VAR_NAME, raising=False)
    with pytest.raises(EnvironmentError):
        load_required_str_env_var(VAR_NAME)


@pytest.mark.parametrize('value', ['true', 'True', 'TRUE'])
def test_load_required_bool_env_var_true_is_case_insensitive(monkeypatch, value):
    monkeypatch.setenv(VAR_NAME, value)
    assert load_required_bool_env_var(VAR_NAME) is True


def test_load_required_bool_env_var_false(monkeypatch):
    monkeypatch.setenv(VAR_NAME, 'false')
    assert load_required_bool_env_var(VAR_NAME) is False


def test_load_required_bool_env_var_invalid_raises(monkeypatch):
    monkeypatch.setenv(VAR_NAME, 'yes')
    with pytest.raises(EnvironmentError, match="must be 'true' or 'false'"):
        load_required_bool_env_var(VAR_NAME)


def test_load_required_bool_env_var_missing_raises(monkeypatch):
    monkeypatch.delenv(VAR_NAME, raising=False)
    with pytest.raises(EnvironmentError):
        load_required_bool_env_var(VAR_NAME)


def test_load_required_int_env_var_returns_int(monkeypatch):
    monkeypatch.setenv(VAR_NAME, '42')
    assert load_required_int_env_var(VAR_NAME) == 42


def test_load_required_int_env_var_invalid_raises_with_cause(monkeypatch):
    monkeypatch.setenv(VAR_NAME, 'abc')
    with pytest.raises(EnvironmentError) as exc_info:
        load_required_int_env_var(VAR_NAME)
    assert isinstance(exc_info.value.__cause__, ValueError)


def test_load_required_int_env_var_missing_raises(monkeypatch):
    monkeypatch.delenv(VAR_NAME, raising=False)
    with pytest.raises(EnvironmentError):
        load_required_int_env_var(VAR_NAME)


def test_load_required_path_env_var_existing_path(monkeypatch, tmp_path):
    monkeypatch.setenv(VAR_NAME, str(tmp_path))
    assert load_required_path_env_var(VAR_NAME) == tmp_path


def test_load_required_path_env_var_missing_path_raises(monkeypatch, tmp_path):
    monkeypatch.setenv(VAR_NAME, str(tmp_path / 'does-not-exist'))
    with pytest.raises(EnvironmentError, match='does not exist'):
        load_required_path_env_var(VAR_NAME)


def test_load_required_path_env_var_unset_raises(monkeypatch):
    monkeypatch.delenv(VAR_NAME, raising=False)
    with pytest.raises(EnvironmentError):
        load_required_path_env_var(VAR_NAME)


def test_load_calculated_env_paths_success(tmp_path):
    with patch('audio_fingerprinter.env_var_loader.subprocess.run') as run, \
            patch('audio_fingerprinter.env_var_loader.dotenv.load_dotenv') as load_dotenv:
        load_calculated_env_paths(tmp_path)

        run.assert_called_once()
        args, kwargs = run.call_args
        assert args[0] == ['bash', str(tmp_path / 'scripts/generate-calculated-paths-env-file.sh')]
        assert kwargs['check'] is True
        load_dotenv.assert_called_once_with(tmp_path / 'env/calculated_paths/.env')


def test_load_calculated_env_paths_failure_wraps_error(tmp_path):
    error = subprocess.CalledProcessError(returncode=1, cmd=['bash'], stderr='boom')
    with patch('audio_fingerprinter.env_var_loader.subprocess.run', side_effect=error):
        with pytest.raises(EnvironmentError) as exc_info:
            load_calculated_env_paths(tmp_path)
        assert exc_info.value.__cause__ is error


def test_load_env_vars_from_file_if_exists_missing_file_does_nothing(tmp_path):
    missing_file = tmp_path / 'nonexistent.env'
    with patch('audio_fingerprinter.env_var_loader.dotenv.load_dotenv') as load_dotenv:
        load_env_vars_from_file_if_exists(missing_file)
        load_dotenv.assert_not_called()


def test_load_env_vars_from_file_if_exists_present_file_loads_it(tmp_path):
    env_file = tmp_path / 'present.env'
    env_file.write_text('FOO=bar\n')
    with patch('audio_fingerprinter.env_var_loader.dotenv.load_dotenv') as load_dotenv:
        load_env_vars_from_file_if_exists(env_file)
        load_dotenv.assert_called_once_with(env_file)


def test_load_required_secret_env_var_strips_surrounding_quotes(monkeypatch):
    monkeypatch.setenv(VAR_NAME, '"secret123"')
    assert load_required_secret_env_var(VAR_NAME) == 'secret123'


def test_load_required_secret_env_var_without_quotes_unchanged(monkeypatch):
    monkeypatch.setenv(VAR_NAME, 'secret123')
    assert load_required_secret_env_var(VAR_NAME) == 'secret123'


def test_load_required_secret_env_var_asymmetric_quote_unchanged(monkeypatch):
    monkeypatch.setenv(VAR_NAME, '"secret123')
    assert load_required_secret_env_var(VAR_NAME) == '"secret123'


def test_load_required_secret_env_var_missing_raises(monkeypatch):
    monkeypatch.delenv(VAR_NAME, raising=False)
    with pytest.raises(EnvironmentError):
        load_required_secret_env_var(VAR_NAME)
