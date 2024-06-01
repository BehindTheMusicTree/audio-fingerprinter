#!/usr/bin/env python

import config as config
import unittest
from audio_fingerprint_generator.audio_fingerprint_generator \
    import WrongFileExtensionError, WrongFileTypeError, FpcalcStatus2Error, get_fingerprint_and_duration_from_file

class TestAudioFingerprintGenerator(unittest.TestCase):
    
    def test_file_path_doesnt_exist_then_error(self):
        with self.assertRaises(FileNotFoundError):
            get_fingerprint_and_duration_from_file('path/to/non/existing/file')
        
    def test_mp3_track_then_ok(self):
        _, fingerprint = get_fingerprint_and_duration_from_file('tests/samples/Bonnie Tyler - Total Eclipse of the Heart.mp3')
        assert fingerprint
        
    def test_flac_track_then_ok(self):
        _, fingerprint = get_fingerprint_and_duration_from_file('tests/samples/oostil - drown (massano remix).flac')
        assert fingerprint

    def test_wav_track_then_ok(self):
        _, fingerprint = get_fingerprint_and_duration_from_file('tests/samples/Y do i - Carmina Burana Remix.wav')
        assert fingerprint

    def test_short_mp3_then_depends_on_os(self):
        file_path = 'tests/samples/short.mp3'
        if config.ENV == config.ENV_VALUES.DEV:
            with self.assertRaises(FpcalcStatus2Error):
                get_fingerprint_and_duration_from_file(file_path)
        if config.ENV == config.ENV_VALUES.GITHUB_CI:
            _, fingerprint = get_fingerprint_and_duration_from_file(file_path)
            assert fingerprint == b'AQAAAA'
            
    def test_short_flac_then_depends_on_os(self):
        file_path = 'tests/samples/short.flac'
        if config.ENV == config.ENV_VALUES.DEV:
            with self.assertRaises(FpcalcStatus2Error):
                get_fingerprint_and_duration_from_file(file_path)
        if config.ENV == config.ENV_VALUES.GITHUB_CI:
            _, fingerprint = get_fingerprint_and_duration_from_file(file_path)
            assert fingerprint == b'AQAAAA'
            
    def test_short_wav_then_depends_on_os(self):
        file_path = 'tests/samples/short.wav'
        if config.ENV == config.ENV_VALUES.DEV:
            with self.assertRaises(FpcalcStatus2Error):
                get_fingerprint_and_duration_from_file(file_path)
        if config.ENV == config.ENV_VALUES.GITHUB_CI:
            _, fingerprint = get_fingerprint_and_duration_from_file(file_path)
            assert fingerprint == b'AQAAAA'
            
    def test_wrong_file_extension_then_error(self):
        with self.assertRaises(WrongFileExtensionError):
            get_fingerprint_and_duration_from_file('tests/samples/wrong_extension.mp6')
            
    def test_not_audio_file_then_error(self):
        with self.assertRaises(WrongFileTypeError):
            get_fingerprint_and_duration_from_file('tests/samples/json_file_type.mp3')


if __name__ == '__main__':
    unittest.main()