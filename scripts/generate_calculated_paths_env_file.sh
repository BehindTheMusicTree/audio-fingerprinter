#!/bin/bash

echo "Generating calculated paths env file"
if [ -z "$1" ]; then
    echo "Error: no base dir provided." >&2
    exit 1
fi
BASE_DIR=$1

if [ -z "$2" ]; then
    echo "Error: no calculated paths env file path provided." >&2
    exit 1
fi
GENERATED_PATHS_ENV_FILE=$2

required_vars=("FLASK_LOGS_ARE_NEEDED")
if [ -z "$FLASK_LOGS_ARE_NEEDED" ]; then
    echo "FLASK_LOGS_ARE_NEEDED must be set" >&2
    exit 1
fi
FLASK_LOGS_ARE_NEEDED=$(echo "$FLASK_LOGS_ARE_NEEDED" | tr '[:upper:]' '[:lower:]')

if [ $FLASK_LOGS_ARE_NEEDED != "true" ] && [ $FLASK_LOGS_ARE_NEEDED != "false" ]; then
    echo "FLASK_LOGS_ARE_NEEDED must be set to true or false."
    exit 1
fi

if [ $FLASK_LOGS_ARE_NEEDED = "true" ]; then
    if [ -z "$APP_IS_EXPOSED" ]; then
        echo "APP_IS_EXPOSED must be set" >&2
        exit 1
    fi
    APP_IS_EXPOSED=$(echo "$APP_IS_EXPOSED" | tr '[:upper:]' '[:lower:]')

    if [ $APP_IS_EXPOSED != "true" ] && [ $APP_IS_EXPOSED != "false" ]; then
        echo "APP_IS_EXPOSED must be set to true or false" >&2
        exit 1
    fi

    if [ $APP_IS_EXPOSED = "true" ]; then
        echo "APP_IS_EXPOSED is set to true"
        if [ -z "$FLASK_LOG_DIR" ]; then
            echo "FLASK_LOG_DIR must be set" >&2
            exit 1
        fi
    else
        echo "APP_IS_EXPOSED is set to false"
        if [ -z "$FLASK_LOG_INTERNAL_DIR" ]; then
            echo "FLASK_LOG_INTERNAL_DIR must be set" >&2
            exit 1
        fi
        FLASK_LOG_DIR=${BASE_DIR}${FLASK_LOG_INTERNAL_DIR}
    fi

    if [ -f $GENERATED_PATHS_ENV_FILE ]; then
        rm -f $GENERATED_PATHS_ENV_FILE
    fi
    touch $GENERATED_PATHS_ENV_FILE

    echo "FLASK_LOG_DIR: $FLASK_LOG_DIR"
    echo "FLASK_LOG_DIR=$FLASK_LOG_DIR" >> "$GENERATED_PATHS_ENV_FILE"
fi