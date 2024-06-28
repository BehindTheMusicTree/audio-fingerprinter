#!/usr/bin/env python

import json
import os
import re


class CONFIG_KEYS:
    class ENV:
        NAME = 'NAME'
        DEBUG = 'DEBUG'
        EXTERNAL_LOG_NEEDED = 'EXTERNAL_DIRS_NEEDED'
        LOG_LEVEL = 'LOG_LEVEL'

    class INTERNAL_PATHS:
        POOL = 'POOL'
        LOG_DEFAULT = 'LOG_DEFAULT'


CONFIG_SETTINGS_FILE = 'config/env_config.json'


def load_config(config_path=CONFIG_SETTINGS_FILE):
    """Load the configurations from a JSON file."""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise EnvironmentError(f"The configuration file '{config_path}' was not found.")


CONFIG_WITH_KEYS_IN_CAMEL_CASE = load_config()


def transform_all_keys_from_lower_camel_case_to_capital_snake_case(dictionary):
    if isinstance(dictionary, dict):
        return {
            transform_key_from_lower_camel_case_to_capital_snake_case(k):
            transform_all_keys_from_lower_camel_case_to_capital_snake_case(v) for k, v in dictionary.items()
        }
    elif isinstance(dictionary, list):
        return [transform_all_keys_from_lower_camel_case_to_capital_snake_case(item) for item in dictionary]
    else:
        return dictionary


def transform_key_from_lower_camel_case_to_capital_snake_case(key):
    key = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).upper()


CONFIG = transform_all_keys_from_lower_camel_case_to_capital_snake_case(CONFIG_WITH_KEYS_IN_CAMEL_CASE)

ENVIRONMENTS_CONFIG = CONFIG.get('ENVIRONMENTS', {})

ENV = os.getenv('ENV')
ENV_CONFIG = None
if ENV is None:
    raise EnvironmentError("The ENV variable is not set")
else:
    ENV_CONFIG = ENVIRONMENTS_CONFIG[ENV]
    ENV_CONFIG[CONFIG_KEYS.ENV.NAME] = ENV

INTERNAL_PATHS = CONFIG.get('INTERNAL_PATHS', {})
