#!/usr/bin/env python

import base64
from flask import Flask, request

import config as config
from app.audio_fingerprint_generator \
    import FpcalcStatus2Error, WrongFileExtensionError, WrongFileTypeError, FileNotFoundError, \
    get_fingerprint_and_duration_from_file


def create_app():
    app = Flask(__name__)
    if config.ENV == config.ENV_VALUES.TEST:
        app.config.from_object(config.TestConfig)
    elif config.ENV == config.ENV_VALUES.DEV:
        app.config.from_object(config.DevConfig)
    elif config.ENV == config.ENV_VALUES.GITHUB_CI_TEST:
        app.config.from_object(config.GithubCiTestConfig)
    elif config.ENV == config.ENV_VALUES.PROD:
        app.config.from_object(config.ProdConfig)
    else:
        raise ValueError(f'Invalid ENV value {config.ENV}')

    def error_response(message, status):
        return {'status': status, 'message': message}, status

    class POST_FIELDS:
        FILE_PATH: str = 'filepath'

    class RESPONSE_FIELDS:
        DURATION: str = 'duration'
        FINGERPRINT: str = 'fingerprint'

    @app.route('/generate-audio-fingerprint/', methods=['POST'])
    def generate_audio_fingerprint():
        if POST_FIELDS.FILE_PATH not in request.json:
            return error_response('No filepath in the request', 400)
        filepath = request.json[POST_FIELDS.FILE_PATH]
        try:
            duration, fingerprint = get_fingerprint_and_duration_from_file(filepath)
            fingerprint_b64 = base64.b64encode(fingerprint).decode()
            return {RESPONSE_FIELDS.DURATION: duration, RESPONSE_FIELDS.FINGERPRINT: fingerprint_b64}
        except Exception as e:
            error_message = str(e)
            if (isinstance(e, FileNotFoundError) or
                    isinstance(e, WrongFileExtensionError) or
                    isinstance(e, WrongFileTypeError)):
                return error_response(error_message, 400)
            if isinstance(e, FpcalcStatus2Error):
                return error_response(error_message, 422)
            return error_response(error_message, 500)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT)
