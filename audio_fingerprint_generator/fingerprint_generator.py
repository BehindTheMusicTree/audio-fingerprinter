#!/usr/bin/env python

from typing import Optional
import acoustid
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
import tempfile

def get_fingerprint_and_duration_from_file_path(file_path: str) -> tuple[Optional[bytes], Optional[int]]:
    try:
        return acoustid.fingerprint_file(path=file_path)
    except acoustid.FingerprintGenerationError as error:
        if error.args[0] == 'fpcalc exited with status 2':
            raise ValueError('fpcalc exited with status 2. Make sure the file is an audio file and that it is not to short.')
        else:
            raise error

def get_fingerprint_and_duration_from_file(file) -> tuple[Optional[bytes], Optional[int]]:
    if isinstance(file, str):
        return get_fingerprint_and_duration_from_file_path(file)
    elif isinstance(file, InMemoryUploadedFile):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            return get_fingerprint_and_duration_from_file_path(tmp.name)
    elif isinstance(file, TemporaryUploadedFile):
        return get_fingerprint_and_duration_from_file_path(file.file.name)
    else:
        raise TypeError('file must be a file path string, a Django InMemoryUploadedFile or a Django TemporaryUploadedFile')