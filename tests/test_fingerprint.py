#!/usr/bin/env python

import os

import werkzeug
from app.audio_fingerprint_generator import ERROR_CODES_STR
import config as config
import unittest
import json
from dataclasses import dataclass
from marshmallow_dataclass import class_schema
import marshmallow

from run import app


class ResponseObject:
    pass


class OkResponseObject(ResponseObject):
    duration: float
    fingerprint: bytes


class BadRequestResponseObject(ResponseObject):
    status: int
    message: str


class UnprocessableEntityResponseObject(ResponseObject):
    status: int
    message: str


class TestAudioFingerprintGenerator(unittest.TestCase):

    response_object = None

    def setUp(self):
        self.app = app.test_client()

    def post_generate_audio_fingerprint(self, filename) -> ResponseObject:
        file_path = os.getcwd() + "/tests/samples/" + filename
        response = self.app.post('/generate-audio-fingerprint',
                                 data=json.dumps({'filepath': file_path}),
                                 content_type='application/json')

        if response.status_code == 200:
            schema = class_schema(OkResponseObject)()
        elif response.status_code == 400:
            schema = class_schema(BadRequestResponseObject)()
        elif response.status_code == 422:
            schema = class_schema(UnprocessableEntityResponseObject)()
        elif response.status_code == 500:
            print(f"Internal server error: {response.data}")
        else:
            print(f"Unexpected status code: {response.status_code}")

        assert response.status_code in [200, 400, 422]

        if schema:
            try:
                return schema.load(response.json)
            except marshmallow.exceptions.ValidationError as err:
                print(f"Error deserializing JSON to ErrorResponseObject: {err}")

        return ResponseObject()

    def test_file_path_doesnt_exist_then_error(self):
        response = self.post_generate_audio_fingerprint('path/to/non/existing/file')
        self.assertEqual(type(response), BadRequestResponseObject)
        if type(response) == BadRequestResponseObject:
            assert ERROR_CODES_STR.FILE_NOT_FOUND in response.message

    def test_mp3_track_then_ok(self):
        response = self.post_generate_audio_fingerprint('Bonnie Tyler - Total Eclipse of the Heart.mp3')
        assert type(response) is OkResponseObject
        assert response.fingerprint

    def test_flac_track_then_ok(self):
        response = self.post_generate_audio_fingerprint('oostil - drown (massano remix).flac')
        assert type(response) is OkResponseObject
        assert response.fingerprint

    def test_wav_track_then_ok(self):
        response = self.post_generate_audio_fingerprint('Y do i - Carmina Burana Remix.wav')
        assert type(response) is OkResponseObject
        assert response.fingerprint

    def test_short_mp3_then_depends_on_os(self):
        response = self.post_generate_audio_fingerprint('short.mp3')
        if config.ENV == config.ENV_VALUES.DEV:
            assert type(response) is UnprocessableEntityResponseObject
        if config.ENV == config.ENV_VALUES.GITHUB_CI_TEST:
            assert type(response) is OkResponseObject
            assert response.fingerprint == b'AQAAAA'

    def test_short_flac_then_depends_on_os(self):
        response = self.post_generate_audio_fingerprint('short.flac')
        if config.ENV == config.ENV_VALUES.DEV:
            assert type(response) is UnprocessableEntityResponseObject
        if config.ENV == config.ENV_VALUES.GITHUB_CI_TEST:
            assert type(response) is OkResponseObject
            assert response.fingerprint == b'AQAAAA'

    def test_short_wav_then_depends_on_os(self):
        response = self.post_generate_audio_fingerprint('short.wav')
        if config.ENV == config.ENV_VALUES.DEV:
            assert type(response) is UnprocessableEntityResponseObject
        if config.ENV == config.ENV_VALUES.GITHUB_CI_TEST:
            assert type(response) is OkResponseObject
            assert response.fingerprint == b'AQAAAA'

    def test_wrong_file_extension_then_error(self):
        response = self.post_generate_audio_fingerprint('wrong_extension.mp6')
        assert type(response) is BadRequestResponseObject
        assert ERROR_CODES_STR.WRONG_FILE_EXTENSION in response.message

    def test_not_audio_file_then_error(self):
        response = self.post_generate_audio_fingerprint('json_file_type.mp3')
        assert type(response) is BadRequestResponseObject
        assert ERROR_CODES_STR.WRONG_FILE_TYPE in response.message

    if __name__ == '__main__':
        unittest.main()
