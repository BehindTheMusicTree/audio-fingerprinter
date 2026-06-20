#!/usr/bin/env python

from unittest.mock import patch

import pydub.exceptions
import pytest
import acoustid

import settings
from audio_fingerprinter.audio_fingerprinter import get_fingerprint_and_duration_from_filename
from audio_fingerprinter.errors import FpcalcStatus2Error, WrongFileTypeError


@pytest.fixture
def audio_file(tmp_path):
    file_path = tmp_path / 'sample.mp3'
    file_path.write_bytes(b'')
    return str(file_path)


def test_happy_path_returns_fingerprint_unchanged(audio_file):
    with patch('audio_fingerprinter.audio_fingerprinter.pydub.AudioSegment.from_file') as from_file, \
            patch('audio_fingerprinter.audio_fingerprinter.acoustid.fingerprint_file') as fingerprint_file:
        fingerprint_file.return_value = (12.3, b'fingerprint-bytes')

        result = get_fingerprint_and_duration_from_filename(audio_file)

        assert result == (12.3, b'fingerprint-bytes')
        from_file.assert_called_once()
        fingerprint_file.assert_called_once_with(path=audio_file)


def test_couldnt_decode_error_dev_env_raises_wrong_file_type(audio_file, monkeypatch):
    monkeypatch.setattr(settings, 'ENV', settings.EnvValues.DEV)
    with patch('audio_fingerprinter.audio_fingerprinter.pydub.AudioSegment.from_file') as from_file:
        from_file.side_effect = pydub.exceptions.CouldntDecodeError('decoding failed with error code: 183')

        with pytest.raises(WrongFileTypeError):
            get_fingerprint_and_duration_from_filename(audio_file)


def test_couldnt_decode_error_non_dev_env_raises_wrong_file_type(audio_file, monkeypatch):
    monkeypatch.setattr(settings, 'ENV', settings.EnvValues.CI_TEST)
    with patch('audio_fingerprinter.audio_fingerprinter.pydub.AudioSegment.from_file') as from_file:
        from_file.side_effect = pydub.exceptions.CouldntDecodeError('decoding failed with error code: 1')

        with pytest.raises(WrongFileTypeError):
            get_fingerprint_and_duration_from_filename(audio_file)


def test_couldnt_decode_error_matching_neither_condition_falls_through(audio_file, monkeypatch):
    # DEV env but the error code doesn't match the DEV-specific '183' condition, and the
    # function has no other branch for it: it neither raises nor re-raises, it just falls
    # through to the acoustid call. This pins down that (possibly unintended) behavior.
    monkeypatch.setattr(settings, 'ENV', settings.EnvValues.DEV)
    with patch('audio_fingerprinter.audio_fingerprinter.pydub.AudioSegment.from_file') as from_file, \
            patch('audio_fingerprinter.audio_fingerprinter.acoustid.fingerprint_file') as fingerprint_file:
        from_file.side_effect = pydub.exceptions.CouldntDecodeError('decoding failed with error code: 1')
        fingerprint_file.return_value = (1.0, b'sentinel')

        result = get_fingerprint_and_duration_from_filename(audio_file)

        assert result == (1.0, b'sentinel')


def test_non_couldnt_decode_error_is_reraised(audio_file):
    with patch('audio_fingerprinter.audio_fingerprinter.pydub.AudioSegment.from_file') as from_file, \
            patch('audio_fingerprinter.audio_fingerprinter.acoustid.fingerprint_file') as fingerprint_file:
        from_file.side_effect = ValueError('boom')

        with pytest.raises(ValueError, match='boom'):
            get_fingerprint_and_duration_from_filename(audio_file)

        fingerprint_file.assert_not_called()


def test_fpcalc_status_2_is_converted_to_app_error(audio_file):
    with patch('audio_fingerprinter.audio_fingerprinter.pydub.AudioSegment.from_file'), \
            patch('audio_fingerprinter.audio_fingerprinter.acoustid.fingerprint_file') as fingerprint_file:
        fingerprint_file.side_effect = acoustid.FingerprintGenerationError('fpcalc exited with status 2')

        with pytest.raises(FpcalcStatus2Error):
            get_fingerprint_and_duration_from_filename(audio_file)


def test_other_fingerprint_generation_error_is_reraised(audio_file):
    with patch('audio_fingerprinter.audio_fingerprinter.pydub.AudioSegment.from_file'), \
            patch('audio_fingerprinter.audio_fingerprinter.acoustid.fingerprint_file') as fingerprint_file:
        fingerprint_file.side_effect = acoustid.FingerprintGenerationError('some other failure')

        with pytest.raises(acoustid.FingerprintGenerationError, match='some other failure'):
            get_fingerprint_and_duration_from_filename(audio_file)
