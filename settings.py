#!/usr/bin/env python

import logging
import os
from pathlib import Path
import subprocess
import dotenv

BASE_DIR = Path(__file__).resolve().parent

APP_ENV_FILE_RELATIVE_PATH = os.getenv('ENV_FILE', BASE_DIR / 'env/.env')
APP_ENV_FILE = BASE_DIR / APP_ENV_FILE_RELATIVE_PATH

if not APP_ENV_FILE.exists():
    print(f"No env file at {APP_ENV_FILE}")
    APP_ENV_FILE = None
else:
    print("Env file provided. Loading.")
    dotenv.load_dotenv(APP_ENV_FILE)


class ENV_NAMES:
    DEV = 'DEV'
    CI_TEST = 'CI_TEST'
    TEST = 'TEST'
    PROD = 'PROD'


ENV = os.getenv('ENV')
if not ENV:
    raise EnvironmentError('ENV must be set')

DEBUG = os.getenv('DEBUG')
if DEBUG is None:
    raise EnvironmentError('DEBUG must be set')
if DEBUG.lower() not in ['true', 'false']:
    raise EnvironmentError('DEBUG must be either true or false')
DEBUG = DEBUG.lower() == 'true'

CALCULATED_PATHS_ENV_FILE = BASE_DIR / 'env/calculated_paths/.env'
generate_calculated_paths_env_file_script_path = BASE_DIR / 'scripts/generate_calculated_paths_env_file.sh'
try:
    result = subprocess.run(['bash', str(generate_calculated_paths_env_file_script_path),
                             str(BASE_DIR) + '/',
                             CALCULATED_PATHS_ENV_FILE,
                             APP_ENV_FILE or ""],
                            check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            env=os.environ.copy())
    print("Paths env file generated.")
    print("Output:", result.stdout)
except subprocess.CalledProcessError as e:
    print("Error while generating the paths env file:", e.stderr)
    raise EnvironmentError("Error while generating the paths env file: " + str(e)) from e

dotenv.load_dotenv(CALCULATED_PATHS_ENV_FILE)

APP_PORT_STR = os.getenv('APP_PORT')
if not APP_PORT_STR:
    raise EnvironmentError('APP_PORT must be set')
if not APP_PORT_STR.isdigit():
    raise EnvironmentError('APP_PORT must be a number')
APP_PORT = int(APP_PORT_STR)

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

SAMPLE_DIR = BASE_DIR / 'test/samples'
if not os.path.isdir(SAMPLE_DIR):
    print(f"The dir {SAMPLE_DIR} must be created.")

POOL_DIR = os.getenv('POOL_DIR')
if not POOL_DIR:
    raise EnvironmentError('POOL_DIR must be set')
if not os.path.isdir(POOL_DIR):
    print(f"The dir {POOL_DIR} must be created.")
print("Setting pool dir to: " + str(POOL_DIR))

LOGS_ARE_NEEDED = os.getenv('FLASK_LOGS_ARE_NEEDED')
if not LOGS_ARE_NEEDED:
    raise EnvironmentError('LOGS_ARE_NEEDED must be set')
if LOGS_ARE_NEEDED.lower() not in ['true', 'false']:
    raise EnvironmentError('LOGS_ARE_NEEDED must be either true or false')
LOGS_ARE_NEEDED = LOGS_ARE_NEEDED.lower() == 'true'

if LOGS_ARE_NEEDED:
    LOG_DIR_ENV = os.getenv('FLASK_LOG_DIR')
    if not LOG_DIR_ENV:
        raise EnvironmentError('LOG_DIR must be set')
    LOG_DIR = Path(LOG_DIR_ENV)
    if not os.path.isdir(LOG_DIR):
        print(f"The dir {LOG_DIR} must be created.")
    print("Setting log dir to: " + str(LOG_DIR))

    LOG_APP_FILENAME = os.getenv('FLASK_LOG_APP_FILENAME')
    if not LOG_APP_FILENAME:
        raise EnvironmentError('FLASK_LOG_APP_FILENAME must be set')
    LOG_APP_FILE = LOG_DIR / LOG_APP_FILENAME
    if not os.path.isfile(LOG_APP_FILE):
        raise EnvironmentError(f"The file {LOG_APP_FILE} must be created.")

    LOG_ERROR_FILENAME = os.getenv('FLASK_LOG_ERROR_FILENAME')
    if not LOG_ERROR_FILENAME:
        raise EnvironmentError('FLASK_LOG_ERROR_FILENAME must be set')
    LOG_ERROR_FILE = LOG_DIR / LOG_ERROR_FILENAME
    if not os.path.isfile(LOG_ERROR_FILE):
        raise EnvironmentError(f"The file {LOG_ERROR_FILE} must be created.")

    LOG_REQUESTS_FILENAME = os.getenv('FLASK_LOG_REQUESTS_FILENAME')
    if not LOG_REQUESTS_FILENAME:
        raise EnvironmentError('FLASK_LOG_REQUESTS_FILENAME must be set')
    LOG_REQUESTS_FILE = LOG_DIR / LOG_REQUESTS_FILENAME
    if not os.path.isfile(LOG_REQUESTS_FILE):
        raise EnvironmentError(f"The file {LOG_REQUESTS_FILE} must be created.")

    if DEBUG:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
else:
    LOG_DIR = None
    LOG_APP_FILE = None
    LOG_ERROR_FILE = None
    LOG_REQUESTS_FILE = None
    LOG_LEVEL = None
    print("Logs are not needed.")

FPCALC = os.getenv('FPCALC')
if not FPCALC:
    raise EnvironmentError('FPCALC must be set')
if not os.path.isfile(FPCALC):
    raise EnvironmentError(f"{FPCALC} is not a valid path for fpcalc.")
