#!/usr/bin/env python

from audio_fingerprinter.errors import FpcalcStatus2Error, WrongFileTypeError
import settings
import os
from typing import Optional, Tuple
import acoustid
import pydub

import pydub.exceptions


def get_fingerprint_and_duration_from_filename(file_path: str) -> Tuple[Optional[float], Optional[bytes]]:

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
