#!/usr/bin/env python

import base64
import os


from app.audio_fingerprint_generator import ERROR_CODES_STR
import config as config
import unittest
import json
from marshmallow_dataclass import class_schema
import marshmallow
from marshmallow import Schema, fields

from run import app


class ResponseObject:
    pass


class OkResponseObjectSchema(Schema):
    duration = fields.Float(required=True)
    fingerprint_str = fields.Str(required=False)
    fingerprint = fields.String(required=True, base64=True)


class OkResponseObject(ResponseObject):
    def __init__(self, data: dict):
        self.duration = data.get('duration')
        self.fingerprint_str = data.get('fingerprint_str')
        data_fingerprint = data.get('fingerprint')
        if not data_fingerprint:
            raise ValueError('No fingerprint in the data')
        self.fingerprint = base64.b64decode(data_fingerprint)


class BadRequestResponseObject(ResponseObject):
    status: int
    message: str


class UnprocessableEntityResponseObject(ResponseObject):
    status: int
    message: str


class TestAudioFingerprinter(unittest.TestCase):

    response_object = None

    def setUp(self):
        self.app = app.test_client()

    def copy_file_to_files_to_pool(self, filename: str):
        file_abs_path_in_test_samples_dir = os.path.join(config.BASE_DIR, "test/samples", filename)
        file_abs_path_in_pool_dir = os.path.join(config.AUDIO_FINGERPRINT_POOL_DIR_ABS_PATH, filename)
        os.system(f"cp '{file_abs_path_in_test_samples_dir}' '{file_abs_path_in_pool_dir}'")

    def remove_file_from_pool(self, filename: str):
        file_path = os.path.join(config.AUDIO_FINGERPRINT_POOL_DIR_ABS_PATH, filename)
        os.system(f"rm '{file_path}'")

    def post_fingerprint_audio(self, filename, testing_missing_file=False) -> ResponseObject:

        if not testing_missing_file:
            self.copy_file_to_files_to_pool(filename)
        response = self.app.post('/fingerprint-audio/',
                                 data=json.dumps({'filename': filename}),
                                 content_type='application/json')

        response_object = None
        if response.status_code == 200:
            schema = OkResponseObjectSchema()
            if response.json is None:
                raise Exception('No JSON in the response')
            data = schema.load(response.json)

            if not isinstance(data, dict):
                raise Exception('Data is not a dictionary')

            response_object = OkResponseObject(data)
        elif response.status_code == 400:
            schema = class_schema(BadRequestResponseObject)()
        elif response.status_code == 422:
            schema = class_schema(UnprocessableEntityResponseObject)()
        elif response.status_code == 500:
            print(f"Internal server error: {response.data}")
        else:
            print(f"Unexpected status code: {response.status_code}")

        assert response.status_code in [200, 400, 422]

        if not response_object and schema:
            try:
                response_object = schema.load(response.json)  # type: ignore
            except marshmallow.exceptions.ValidationError as err:
                print(f"Error deserializing JSON to ErrorResponseObject: {err}")

        if not testing_missing_file:
            self.remove_file_from_pool(filename)

        if isinstance(response_object, ResponseObject):
            return response_object
        return ResponseObject()

    def test_file_path_doesnt_exist_then_error(self):
        response = self.post_fingerprint_audio(filename='non_existent_file.mp3', testing_missing_file=True)
        self.assertEqual(type(response), BadRequestResponseObject)
        if type(response) == BadRequestResponseObject:
            assert ERROR_CODES_STR.FILE_NOT_FOUND in response.message

    def test_mp3_track_then_ok(self):
        response = self.post_fingerprint_audio('Bonnie Tyler - Total Eclipse of the Heart.mp3')
        assert type(response) is OkResponseObject
        assert response.fingerprint

    def test_flac_track_then_ok(self):
        response = self.post_fingerprint_audio('oostil - drown (massano remix).flac')
        assert type(response) is OkResponseObject
        assert response.fingerprint

    def test_wav_track_then_ok(self):
        response = self.post_fingerprint_audio('Y do i - Carmina Burana Remix.wav')
        assert type(response) is OkResponseObject
        assert response.fingerprint

    def test_short_mp3_then_depends_on_os(self):
        response = self.post_fingerprint_audio('short.mp3')
        if config.ENV == config.ENV_VALUES.DEV:
            assert type(response) is UnprocessableEntityResponseObject
        if config.ENV == config.ENV_VALUES.GITHUB_CI_TEST:
            assert type(response) is OkResponseObject
            assert response.fingerprint == b'AQAAAA'

    def test_short_flac_then_depends_on_os(self):
        response = self.post_fingerprint_audio('short.flac')
        if config.ENV == config.ENV_VALUES.DEV:
            assert type(response) is UnprocessableEntityResponseObject
        if config.ENV == config.ENV_VALUES.GITHUB_CI_TEST:
            assert type(response) is OkResponseObject
            assert response.fingerprint == b'AQAAAA'

    def test_short_wav_then_depends_on_os(self):
        response = self.post_fingerprint_audio('short.wav')
        if config.ENV == config.ENV_VALUES.DEV:
            assert type(response) is UnprocessableEntityResponseObject
        if config.ENV == config.ENV_VALUES.GITHUB_CI_TEST:
            assert type(response) is OkResponseObject
            assert response.fingerprint == b'AQAAAA'

    def test_huge_wav_then_ok(self):
        response = self.post_fingerprint_audio('msolo - Sandstorm Remix - 66Mo.wav')
        assert type(response) is OkResponseObject
        assert response.fingerprint

    def test_not_audio_file_then_error(self):
        response = self.post_fingerprint_audio('json_file_type.mp3')
        assert type(response) is BadRequestResponseObject
        assert ERROR_CODES_STR.WRONG_FILE_TYPE in response.message

    # The file is too big to be uploaded on GitHub (100Mo limit)
    # def test_huge_flac_then_ok(self):
    #     response = self.post_generate_audio_fingerprint('Muse - Knights of Cydonia - 147Mo.flac')
    #     assert type(response) is OkResponseObject
    #     assert response.fingerprint

    if __name__ == '__main__':
        unittest.main()
