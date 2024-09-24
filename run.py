#!/usr/bin/env python

import logging
from logging.handlers import RotatingFileHandler
import base64
from os import error
from pathlib import Path
from flask import Flask, request

import settings
from audio_fingerprinter.audio_fingerprinter \
    import FpcalcStatus2Error, WrongFileTypeError, FileNotInPoolError, get_fingerprint_and_duration_from_file_name


def log_fingerprinting_error(user_id, filename, title, message):
    if not user_id:
        user_id = 'unknown'
        message = f'{message} (User ID not provided)'

    if not title:
        title = 'No Title Provided'
        message = f'{message} (Title not provided)'

    app.logger.error(
        '%s: %s. User ID: %s, Filename: %s, Request data: %s',
        title,
        message,
        user_id,
        filename,
        request.json
    )


def create_app():
    app = Flask(__name__)

    if settings.LOG_DIR:
        if not isinstance(settings.LOG_APP_FILE, (str, Path)):
            raise TypeError("LOG_APP_FILE must be a string or Path")
        if not isinstance(settings.LOG_REQUESTS_FILE, (str, Path)):
            raise TypeError("LOG_REQUESTS_FILE must be a string or Path")
        if not isinstance(settings.LOG_LEVEL, int):
            raise TypeError("LOG_LEVEL must be an int")

        app_log_handler = RotatingFileHandler(settings.LOG_APP_FILE, maxBytes=10240, backupCount=10)
        app_log_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        app_log_handler.setLevel(settings.LOG_LEVEL)
        app.logger.addHandler(app_log_handler)
        app.logger.setLevel(settings.LOG_LEVEL)

        error_log_handler = RotatingFileHandler(settings.LOG_ERROR_FILE, maxBytes=10240, backupCount=10)
        error_log_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        error_log_handler.setLevel(logging.ERROR)
        app.logger.addHandler(error_log_handler)

        request_log_handler = RotatingFileHandler(settings.LOG_REQUESTS_FILE, maxBytes=10240, backupCount=10)
        request_log_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
        ))
        request_log_handler.setLevel(settings.LOG_LEVEL)
        request_logger = logging.getLogger('request')
        request_logger.addHandler(request_log_handler)
        request_logger.setLevel(settings.LOG_LEVEL)

    # Log each request
    @ app.after_request
    def after_request(response):
        if settings.LOG_DIR:
            request_logger.info(
                '%s %s %s %s %s',
                request.remote_addr,
                request.method,
                request.scheme,
                request.full_path,
                response.status
            )
        return response

    # Disable strict slashes in the URL routing rules.
    # When this is set to False, the trailing slash in the URL is optional.
    # This means that Flask will respond to both '/generate-audio-fingerprint' and '/generate-audio-fingerprint/'.
    # If this was set to True (the default), Flask would strictly differentiate between the two URLs.
    app.url_map.strict_slashes = False

    def error_response(message, status):
        return {'status': status, 'message': message}, status

    class PostFields:
        FILENAME: str = 'filename'
        TITLE: str = 'title'
        USER_ID: str = 'userId'

    class ResponseFields:
        DURATION: str = 'duration'
        FINGERPRINT: str = 'fingerprint'

    @ app.route('/fingerprint-audio', methods=['POST'])
    def fingerprint_audio():
        if PostFields.FILENAME not in request.json:  # type: ignore
            return error_response('No filename in the request', 400)

        if not isinstance(request.json, dict):
            return error_response('Request body is not a dictionary', 400)

        filename = request.json[PostFields.FILENAME]
        title = request.json.get(PostFields.TITLE)
        user_id = request.json.get(PostFields.USER_ID)
        try:
            duration, fingerprint = get_fingerprint_and_duration_from_file_name(filename)

            if not isinstance(fingerprint, bytes):
                app.logger.error(
                    'Error fingerprinting: fingerprint is not bytes. Found type: %s. Filename: %s, Request data: %s',
                    type(fingerprint).__name__,
                    filename,
                    request.json
                )
                return error_response('Error fingerprinting: fingerprint is not bytes', 500)

            fingerprint_b64 = base64.b64encode(fingerprint).decode()
            return {ResponseFields.DURATION: duration, ResponseFields.FINGERPRINT: fingerprint_b64}
        except Exception as e:

            if (isinstance(e, FileNotInPoolError) or isinstance(e, WrongFileTypeError)):
                return error_response(str(e), 400)

            if isinstance(e, FpcalcStatus2Error):
                error_message = f"Fpcalc returned status 2. {e}"
                log_fingerprinting_error(user_id=user_id, filename=filename, title=title, message=error_message)
                return error_response(str(e), 422)

            error_message = f"Unhandled exception: {e}"
            log_fingerprinting_error(user_id=user_id, filename=filename, title=title, message=error_message)
            return error_response(error_message, 500)

    @app.route('/trigger-error', methods=['GET'])
    def trigger_error():
        app.logger.error('This is a test error for logging purposes')
        raise Exception('This is a test exception to trigger error logging')

    return app


app = create_app()

if __name__ == '__main__':
    if not isinstance(settings.APP_PORT, int):
        raise TypeError("APP_PORT must be an int")
    app.run(host='0.0.0.0', port=settings.APP_PORT)
