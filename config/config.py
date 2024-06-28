#!/usr/bin/env python

import logging
import os
from pathlib import Path
import dotenv
from config.env_config_loader import ENV_CONFIG, INTERNAL_PATHS, CONFIG_KEYS

dotenv.load_dotenv()


class ENV_NAMES:
    DEV = 'DEV'
    CI_TEST = 'CI_TEST'
    TEST = 'TEST'
    PROD = 'PROD'


APP_PORT = os.getenv('APP_PORT')
if APP_PORT is None:
    raise EnvironmentError('APP_PORT not set')

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / '../'

SAMPLE_DIR = BASE_DIR / 'test/samples'

ENV = ENV_CONFIG.get(CONFIG_KEYS.ENV.NAME)

POOL_DIR = BASE_DIR / INTERNAL_PATHS[CONFIG_KEYS.INTERNAL_PATHS.POOL]
print("Setting pool dir to: " + str(POOL_DIR))
LOG_DIR = BASE_DIR / INTERNAL_PATHS[CONFIG_KEYS.INTERNAL_PATHS.LOG]
print("Setting log dir to: " + str(LOG_DIR))

GENERAL_LOG_FILE = LOG_DIR / 'general.log'
REQUEST_LOG_FILE = LOG_DIR / 'request.log'

LOG_LEVEL = None
if ENV_CONFIG[CONFIG_KEYS.ENV.DEBUG]:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO
