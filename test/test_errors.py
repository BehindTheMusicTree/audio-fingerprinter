#!/usr/bin/env python

from audio_fingerprinter.errors import (
    AFP_ERROR_CODES_PREFIXE,
    AppError,
    ErrorCodesStr,
    FileNotInPoolError,
    FpcalcStatus2Error,
    WrongFileTypeError,
)


def test_app_error_formats_code_and_message():
    error = AppError('CODE', 'msg')
    assert str(error) == 'CODE: msg'
    assert isinstance(error, Exception)


def test_fpcalc_status_2_error():
    error = FpcalcStatus2Error('fpcalc failed')
    assert str(error) == f'{ErrorCodesStr.FPCALC_STATUS_2}: fpcalc failed'
    assert isinstance(error, AppError)


def test_wrong_file_type_error():
    error = WrongFileTypeError('not audio')
    assert str(error) == f'{ErrorCodesStr.WRONG_FILE_TYPE}: not audio'
    assert isinstance(error, AppError)


def test_file_not_in_pool_error():
    error = FileNotInPoolError('missing file')
    assert str(error) == f'{ErrorCodesStr.FILE_NOT_IN_POOL}: missing file'
    assert isinstance(error, AppError)


def test_error_codes_are_distinct_and_prefixed():
    codes = [
        ErrorCodesStr.FPCALC_STATUS_2,
        ErrorCodesStr.WRONG_FILE_EXTENSION,
        ErrorCodesStr.WRONG_FILE_TYPE,
        ErrorCodesStr.FILE_NOT_IN_POOL,
    ]
    assert len(set(codes)) == len(codes)
    assert all(code.startswith(AFP_ERROR_CODES_PREFIXE) for code in codes)
