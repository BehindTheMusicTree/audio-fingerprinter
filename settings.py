#!/usr/bin/env python

import logging
import os
from pathlib import Path
from audio_fingerprinter.utils import print_flask
from audio_fingerprinter.env_var_loader import load_calculated_env_paths, load_env_vars_from_file_if_exists, load_required_bool_env_var, \
    load_required_int_env_var, load_required_path_env_var, load_required_str_env_var


class EnvValues:
    DEV = 'DEV'
    CI_TEST = 'CI_TEST'
    TEST = 'TEST'
    PROD = 'PROD'


print_flask("Loading settings...")

BASE_DIR = Path(__file__).resolve().parent
print_flask(f"BASE_DIR: {BASE_DIR}")

APP_ENV_FILE_RELATIVE_PATH = os.getenv('ENV_FILE', 'env/.env')
APP_ENV_FILE = BASE_DIR / APP_ENV_FILE_RELATIVE_PATH
load_env_vars_from_file_if_exists(APP_ENV_FILE)

ENV = load_required_str_env_var('ENV')
DEBUG = load_required_bool_env_var('DEBUG')
APP_PORT = load_required_int_env_var('APP_PORT')

load_calculated_env_paths(BASE_DIR)

SAMPLE_DIR = BASE_DIR / 'test/samples'
if not os.path.isdir(SAMPLE_DIR):
    print(f"The dir {SAMPLE_DIR} must be created.")

POOL_DIR = load_required_path_env_var('POOL_DIR')

LOG_DIR_STR = os.getenv('FLASK_LOG_DIR')
if not LOG_DIR_STR:
    print_flask("FLASK_LOG_DIR is not set. Logs are not needed.")
    LOG_DIR = None
    LOG_APP_FILE = None
    LOG_ERROR_FILE = None
    LOG_REQUESTS_FILE = None
    LOG_LEVEL = None
else:
    print_flask("FLASK_LOG_DIR is set. Setting up logs...")
    LOG_DIR = Path(LOG_DIR_STR)
    if not os.path.isdir(LOG_DIR):
        raise EnvironmentError(f"The dir {LOG_DIR} does not exist.")
    print_flask(f"Setting logs dir to: {LOG_DIR}) .")

    LOG_APP_FILENAME = load_required_str_env_var('FLASK_LOG_APP_FILENAME')
    LOG_APP_FILE = LOG_DIR / LOG_APP_FILENAME
    if not os.path.isfile(LOG_APP_FILE):
        raise EnvironmentError(f"The file {LOG_APP_FILE} must be created.")

    LOG_ERROR_FILENAME = load_required_str_env_var('FLASK_LOG_ERROR_FILENAME')
    if not LOG_ERROR_FILENAME:
        raise EnvironmentError('FLASK_LOG_ERROR_FILENAME must be set')
    LOG_ERROR_FILE = LOG_DIR / LOG_ERROR_FILENAME
    if not os.path.isfile(LOG_ERROR_FILE):
        raise EnvironmentError(f"The file {LOG_ERROR_FILE} must be created.")

    LOG_REQUESTS_FILENAME = load_required_str_env_var('FLASK_LOG_REQUESTS_FILENAME')
    if not LOG_REQUESTS_FILENAME:
        raise EnvironmentError('FLASK_LOG_REQUESTS_FILENAME must be set')
    LOG_REQUESTS_FILE = LOG_DIR / LOG_REQUESTS_FILENAME
    if not os.path.isfile(LOG_REQUESTS_FILE):
        raise EnvironmentError(f"The file {LOG_REQUESTS_FILE} must be created.")

    if DEBUG:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO

FPCALC = load_required_path_env_var('FPCALC')
