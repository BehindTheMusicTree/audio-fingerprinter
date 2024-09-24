#!/usr/bin/env python

import settings
import os
from typing import Optional, Tuple
import acoustid
import pydub

import pydub.exceptions

AFP_ERROR_CODES_PREFIXE = 'Audio Fingerprinter Error Code '


class ERROR_CODES_STR:
    FPCALC_STATUS_2 = AFP_ERROR_CODES_PREFIXE + '1'
    WRONG_FILE_EXTENSION = AFP_ERROR_CODES_PREFIXE + '2'
    WRONG_FILE_TYPE = AFP_ERROR_CODES_PREFIXE + '3'
    FILE_NOT_IN_POOL = AFP_ERROR_CODES_PREFIXE + '4'


class AppError(Exception):

    def __init__(self, code_str: str, message: str) -> None:
        super().__init__(f"{code_str}: {message}")


class FpcalcStatus2Error(AppError):

    def __init__(self, message: str) -> None:
        super().__init__(ERROR_CODES_STR.FPCALC_STATUS_2, message)


class WrongFileTypeError(AppError):

    def __init__(self, message: str) -> None:
        super().__init__(ERROR_CODES_STR.WRONG_FILE_TYPE, message)


class FileNotInPoolError(AppError):

    def __init__(self, message: str) -> None:
        super().__init__(ERROR_CODES_STR.FILE_NOT_IN_POOL, message)


def get_fingerprint_and_duration_from_file_name(file_name: str) -> Tuple[Optional[float], Optional[bytes]]:
    file_path = os.path.join(settings.POOL_DIR, file_name)

    if not os.path.exists(file_path):
        raise FileNotInPoolError(f'The file {file_name} is not located in the Audio Fingerprint pool directory.')

    _, extension = os.path.splitext(file_path)

    try:
        with open(file_path, 'rb') as f:
            pydub.AudioSegment.from_file(f, format=extension[1:])
    except Exception as error:
        if isinstance(error, pydub.exceptions.CouldntDecodeError):
            first_error = error.args[0]
            if (settings.ENV == settings.EnvValues.DEV and 'error code: 183' in first_error) or \
                    (settings.ENV != settings.EnvValues.DEV and 'error code: 1' in first_error):
                raise WrongFileTypeError(f'Invalid file type. Only audio types are allowed.')
        else:
            raise error

    try:
        return acoustid.fingerprint_file(path=file_path)
    except acoustid.FingerprintGenerationError as error:
        if error.args[0] == 'fpcalc exited with status 2':
            raise FpcalcStatus2Error(
                'fpcalc exited with status 2. Make sure the file is an audio is not corrupted. ' +
                'On MacOS, it may mean that the audio file is too short for a fingerprint to be generated.')
        else:
            raise error
