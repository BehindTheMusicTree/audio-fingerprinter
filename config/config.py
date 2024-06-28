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


if ENV_CONFIG.get(CONFIG_KEYS.ENV.EXTERNAL_LOG_NEEDED):
    LOG_DIR_ENV = os.getenv('LOG_DIR')
    if LOG_DIR_ENV is None:
        raise EnvironmentError("The LOG_DIR variable is not set")
    else:
        LOG_DIR = Path(LOG_DIR_ENV)
        print("Setting log dir to: " + str(LOG_DIR))
else:
    LOG_DIR = BASE_DIR / INTERNAL_PATHS.get(CONFIG_KEYS.INTERNAL_PATHS.LOG_DEFAULT)
    print("Setting log dir to default: " + str(LOG_DIR))

LOG_LEVEL = None
if ENV_CONFIG[CONFIG_KEYS.ENV.DEBUG]:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

GENERAL_LOG_FILE = LOG_DIR / 'general.log'
REQUEST_LOG_FILE = LOG_DIR / 'request.log'
