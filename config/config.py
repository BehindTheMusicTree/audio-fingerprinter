#!/usr/bin/env python

import logging
import os
from pathlib import Path
import dotenv
from config.config_settings_loader import ENV_NAMES, ENV_CONFIG, DEFAULT_INTERNAL_PATHS, CONFIG_KEYS

dotenv.load_dotenv()

APP_PORT = os.getenv('APP_PORT')
if APP_PORT is None:
    raise EnvironmentError('APP_PORT not set')

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / '../'

SAMPLE_DIR = BASE_DIR / 'test/samples'

ENV = ENV_CONFIG.get(CONFIG_KEYS.ENV.NAME)
if ENV_CONFIG.get(CONFIG_KEYS.ENV.EXTERNAL_DIRS_NEEDED):
    POOL_DIR_ENV = os.getenv('POOL_DIR')
    if POOL_DIR_ENV is None:
        raise EnvironmentError("The POOL_DIR variable is not set")
    else:
        POOL_DIR = Path(POOL_DIR_ENV)
        print("Setting media root to: " + str(POOL_DIR))

    LOG_DIR_ENV = os.getenv('LOG_DIR')
    if LOG_DIR_ENV is None:
        raise EnvironmentError("The LOG_DIR variable is not set")
    else:
        LOG_DIR = Path(LOG_DIR_ENV)
        print("Setting log dir to: " + str(LOG_DIR))
else:
    POOL_DIR = BASE_DIR / DEFAULT_INTERNAL_PATHS.get(CONFIG_KEYS.DEFAULT_INTERNAL_PATHS.POOL)
    print("Setting media dir to default: " + str(POOL_DIR))

    LOG_DIR = BASE_DIR / DEFAULT_INTERNAL_PATHS.get(CONFIG_KEYS.DEFAULT_INTERNAL_PATHS.LOG)
    print("Setting log dir to default: " + str(LOG_DIR))

LOG_LEVEL = None
if ENV_CONFIG[CONFIG_KEYS.ENV.DEBUG]:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

GENERAL_LOG_FILE = LOG_DIR / 'general.log'
REQUEST_LOG_FILE = LOG_DIR / 'request.log'
