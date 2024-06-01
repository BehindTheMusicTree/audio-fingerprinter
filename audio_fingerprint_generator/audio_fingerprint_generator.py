#!/usr/bin/env python

import os
from typing import Optional, Tuple
import acoustid
import pydub
import mimetypes
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
import tempfile

import pydub.exceptions

class AudioFileProbablyTooShortForFingerprintGenerationError(Exception):
    pass

class WrongFileExtensionError(Exception):
    pass

class WrongFileTypeError(Exception):
    pass

def get_fingerprint_and_duration_from_file_path(file_path: str) -> Tuple[Optional[float], Optional[bytes]]:
    _, extension = os.path.splitext(file_path)
    
    mime_type = mimetypes.guess_type(file_path)[0]
    if mime_type is None or not mime_type.startswith('audio/'):
        raise WrongFileExtensionError(f'Invalid file type {mime_type}. Only audio types are allowed.')

    try:
        with open(file_path, 'rb') as f:
            pydub.AudioSegment.from_file(f, format=extension[1:])
    except Exception as error:
        if isinstance(error, pydub.exceptions.CouldntDecodeError) and 'error code: 183' in error.args[0]:            
            raise WrongFileTypeError(f'Invalid file type. Only audio types are allowed.')
        else:
            raise error

    try:
        duration, fingerprint = acoustid.fingerprint_file(path=file_path)
        print(file_path)
        print(f'Fingerprint: {fingerprint}')
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