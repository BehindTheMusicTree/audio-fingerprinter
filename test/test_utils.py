#!/usr/bin/env python

from audio_fingerprinter.utils import print_flask, to_camel_case


def test_to_camel_case_multiple_components():
    assert to_camel_case('hello_world') == 'helloWorld'


def test_to_camel_case_many_components():
    assert to_camel_case('a_b_c') == 'aBC'


def test_to_camel_case_single_component():
    assert to_camel_case('single') == 'single'


def test_print_flask_prefixes_message(capsys):
    print_flask('hello')
    assert '[Flask] hello' in capsys.readouterr().out
