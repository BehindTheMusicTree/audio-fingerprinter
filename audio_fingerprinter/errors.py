#!/usr/bin/env python


AFP_ERROR_CODES_PREFIXE = 'Audio Fingerprinter Error Code '


class ErrorCodesStr:
    FPCALC_STATUS_2 = AFP_ERROR_CODES_PREFIXE + '1'
    WRONG_FILE_EXTENSION = AFP_ERROR_CODES_PREFIXE + '2'
    WRONG_FILE_TYPE = AFP_ERROR_CODES_PREFIXE + '3'
    FILE_NOT_IN_POOL = AFP_ERROR_CODES_PREFIXE + '4'


class AppError(Exception):

    def __init__(self, code_str: str, message: str) -> None:
        super().__init__(f"{code_str}: {message}")


class FpcalcStatus2Error(AppError):

    def __init__(self, message: str) -> None:
        super().__init__(ErrorCodesStr.FPCALC_STATUS_2, message)


class WrongFileTypeError(AppError):

    def __init__(self, message: str) -> None:
        super().__init__(ErrorCodesStr.WRONG_FILE_TYPE, message)


class FileNotInPoolError(AppError):

    def __init__(self, message: str) -> None:
        super().__init__(ErrorCodesStr.FILE_NOT_IN_POOL, message)
