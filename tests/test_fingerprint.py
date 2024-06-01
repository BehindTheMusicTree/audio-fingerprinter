#!/usr/bin/env python

import unittest
from audio_fingerprint_generator.audio_fingerprint_generator \
    import WrongFileExtensionError, WrongFileTypeError, get_fingerprint_and_duration_from_file

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

    def test_short_mp3_then_ok(self):
        _, fingerprint = get_fingerprint_and_duration_from_file('tests/samples/short.mp3')
        assert fingerprint
            
    def test_short_flac_then_ok(self):
        _, fingerprint = get_fingerprint_and_duration_from_file('tests/samples/short.flac')
        assert fingerprint
            
    def test_short_wav_then_ok(self):
        _, fingerprint = get_fingerprint_and_duration_from_file('tests/samples/short.wav')
        assert fingerprint
            
    def test_wrong_file_extension_then_error(self):
        with self.assertRaises(WrongFileExtensionError):
            get_fingerprint_and_duration_from_file('tests/samples/wrong_extension.mp6')
            
    def test_not_audio_file_then_error(self):
        with self.assertRaises(WrongFileTypeError):
            get_fingerprint_and_duration_from_file('tests/samples/json_file_type.mp3')


if __name__ == '__main__':
    unittest.main()