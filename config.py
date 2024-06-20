#!/usr/bin/env python

import logging
import os
import dotenv

dotenv.load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    LOG_LEVEL = logging.INFO
    GENERAL_LOG_FILE = None
    REQUEST_LOG_FILE = None


class DevConfig(Config):
    DEBUG = True
    TESTING = False
    LOG_LEVEL = logging.DEBUG
    GENERAL_LOG_FILE = 'log/general.log'
    REQUEST_LOG_FILE = 'log/request.log'


class GithubCiTestConfig(Config):
    TESTING = True
    DEBUG = False
    LOG_LEVEL = logging.DEBUG
    GENERAL_LOG_FILE = 'log/general.log'
    REQUEST_LOG_FILE = 'log/request.log'


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    GENERAL_LOG_FILE = '/var/log/bodzify-audio-fingerprinter/general.log'
    REQUEST_LOG_FILE = '/var/log/bodzify-audio-fingerprinter/request.log'


class ProdConfig(Config):
    TESTING = False
    DEBUG = False
    LOG_LEVEL = logging.INFO
    GENERAL_LOG_FILE = '/var/log/bodzify-audio-fingerprinter/general.log'
    REQUEST_LOG_FILE = '/var/log/bodzify-audio-fingerprinter/request.log'


class ENV_VALUES:
    DEV = 'DEV'
    CI_TEST = 'CI_TEST'
    TEST = 'TEST'
    PROD = 'PROD'


ENV = os.getenv('ENV')
if ENV is None:
    raise EnvironmentError('ENV not set')

APP_PORT = os.getenv('APP_PORT')
if APP_PORT is None:
    raise EnvironmentError('APP_PORT not set')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUDIO_FINGERPRINT_POOL_DIR_ABS_PATH = '/tmp/bodzify-audio-fingerprinter/pool/'
