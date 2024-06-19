#!/usr/bin/env python

import logging
from logging.handlers import RotatingFileHandler
import base64
from flask import Flask, request

import config as config
from app.audio_fingerprint_generator \
    import FpcalcStatus2Error, WrongFileTypeError, FileNotFoundError, get_fingerprint_and_duration_from_file_name


def create_app():
    app = Flask(__name__)

    if config.ENV == config.ENV_VALUES.DEV:
        app.config.from_object(config.DevConfig)
    elif config.ENV == config.ENV_VALUES.CI_TEST:
        app.config.from_object(config.GithubCiTestConfig)
    elif config.ENV == config.ENV_VALUES.TEST:
        app.config.from_object(config.TestConfig)
    elif config.ENV == config.ENV_VALUES.PROD:
        app.config.from_object(config.ProdConfig)
    else:
        raise ValueError(f'Invalid ENV value {config.ENV}')

    general_log_handler = RotatingFileHandler(app.config['GENERAL_LOG_FILE'], maxBytes=10240, backupCount=10)
    general_log_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))

    general_log_handler.setLevel(app.config['LOG_LEVEL'])
    app.logger.addHandler(general_log_handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])

    request_log_handler = RotatingFileHandler(app.config['REQUEST_LOG_FILE'], maxBytes=10240, backupCount=10)
    request_log_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
    ))
    request_log_handler.setLevel(app.config['LOG_LEVEL'])

    request_logger = logging.getLogger('request')
    request_logger.addHandler(request_log_handler)
    request_logger.setLevel(app.config['LOG_LEVEL'])

    # Log each request
    @app.after_request
    def after_request(response):
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

    class POST_FIELDS:
        FILE_NAME: str = 'filename'

    class RESPONSE_FIELDS:
        DURATION: str = 'duration'
        FINGERPRINT: str = 'fingerprint'

    @app.route('/fingerprint-audio', methods=['POST'])
    def generate_audio_fingerprint():
        if POST_FIELDS.FILE_NAME not in request.json:  # type: ignore
            return error_response('No filename in the request', 400)

        if not isinstance(request.json, dict):
            return error_response('Request body is not a dictionary', 400)

        filename = request.json[POST_FIELDS.FILE_NAME]
        try:
            duration, fingerprint = get_fingerprint_and_duration_from_file_name(filename)

            if not isinstance(fingerprint, bytes):
                return error_response('Error fingerprinting: fingerprint is not bytes', 500)

            fingerprint_b64 = base64.b64encode(fingerprint).decode()
            return {RESPONSE_FIELDS.DURATION: duration, RESPONSE_FIELDS.FINGERPRINT: fingerprint_b64}
        except Exception as e:
            error_message = str(e)
            if (isinstance(e, FileNotFoundError) or isinstance(e, WrongFileTypeError)):
                return error_response(error_message, 400)
            if isinstance(e, FpcalcStatus2Error):
                return error_response(error_message, 422)
            return error_response(error_message, 500)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.APP_PORT)
