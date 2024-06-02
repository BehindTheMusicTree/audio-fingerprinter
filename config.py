#!/usr/bin/env python

import os
import dotenv

dotenv.load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True


class GithubCiTestConfig(Config):
    TESTING = True
    DEBUG = False


class TestConfig(Config):
    TESTING = True
    DEBUG = True


class ProdConfig(Config):
    TESTING = False
    DEBUG = False


class ENV_VALUES:
    DEV = 'DEV'
    GITHUB_CI_TEST = 'GITHUB_CI'
    TEST = 'TEST'
    PROD = 'PROD'


ENV = os.getenv('ENV')
PORT = int(os.getenv('PORT'))  # type: ignore
