#!/usr/bin/env python

import argparse

from audio_fingerprint_generator.audio_fingerprint_generator import get_fingerprint_and_duration_from_file


def main(file_obj):
    duration, fingerprint = get_fingerprint_and_duration_from_file(file_obj)
    print(f'Duration: {duration}, Fingerprint: {fingerprint}')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Generate fingerprint and duration from audio file.')
    parser.add_argument('file', type=str, help='The audio file.')
    args = parser.parse_args()
    main(args.file)