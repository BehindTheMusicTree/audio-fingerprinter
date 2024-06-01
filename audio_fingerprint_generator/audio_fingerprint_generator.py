#!/usr/bin/env python

import os
from typing import Optional, Tuple
import acoustid
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
import tempfile

class AudioFileProbablyTooShortForFingerprintGenerationError(Exception):
    pass

class WrongFileExtensionError(Exception):
    pass

def get_fingerprint_and_duration_from_file_path(file_path: str) -> Tuple[Optional[float], Optional[bytes]]:
    _, extension = os.path.splitext(file_path)
    if extension.lower() not in ['.mp3', '.wav', '.flac']:
        raise WrongFileExtensionError(f'Invalid file extension {extension}. Only .mp3, .wav, and .flac are supported.')

    try:
        return acoustid.fingerprint_file(path=file_path)
    except acoustid.FingerprintGenerationError as error:
        if error.args[0] == 'fpcalc exited with status 2':
            raise AudioFileProbablyTooShortForFingerprintGenerationError(
                'fpcalc exited with status 2. Make sure the file is an audio file and that it is not too short.')
        else:
            raise error

def get_fingerprint_and_duration_from_file(file) -> tuple[Optional[float], Optional[bytes]]:
    if isinstance(file, str):
        file = os.path.expanduser(file)
        if not os.path.exists(file):
            raise FileNotFoundError(f'The file {file} does not exist.')
        return get_fingerprint_and_duration_from_file_path(file)
    elif isinstance(file, InMemoryUploadedFile):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            return get_fingerprint_and_duration_from_file_path(tmp.name)
    elif isinstance(file, TemporaryUploadedFile):
        if not os.path.exists(file.file.name):
            raise FileNotFoundError('The temporary file does not exist.')
        return get_fingerprint_and_duration_from_file_path(file.file.name)
    else:
        raise TypeError('file must be a file path string, a Django InMemoryUploadedFile or a Django TemporaryUploadedFile')