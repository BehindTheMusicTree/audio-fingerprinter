#!/usr/bin/env python

import base64
from flask import Flask, request

import config as config
from audio_fingerprint_generator.audio_fingerprint_generator import FpcalcStatus2Error, WrongFileExtensionError, WrongFileTypeError, get_fingerprint_and_duration_from_file

app = Flask(__name__)

def error_response(message, status):
    return {'status': status, 'message': message}, status

@app.route('/generate-audio-fingerprint', methods=['POST'])
def generate_fingerprint():
    if 'filepath' not in request.json:
        return error_response('No filepath in the request', 400)
    filepath = request.json['filepath']
    try:
        duration, fingerprint = get_fingerprint_and_duration_from_file(filepath)
        fingerprint_b64 = base64.b64encode(fingerprint).decode()
        return {'duration': duration, 'fingerprint': fingerprint_b64}
    except Exception as e:
        error_message = str(e)
        if isinstance(e, FileNotFoundError) or isinstance(e, WrongFileExtensionError) or isinstance(e, WrongFileTypeError):
            return error_response(error_message, 400)
        if isinstance(e, FpcalcStatus2Error):
            return error_response(error_message, 500)
        return error_response(error_message, 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT)