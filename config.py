#!/usr/bin/env python

import os
import dotenv

dotenv.load_dotenv()

class ENV_VALUES:
    DEV = 'DEV'
    GITHUB_CI = 'GITHUB_CI'
    TEST = 'TEST'
    

ENV = os.getenv('ENV')
PORT = os.getenv('PORT')