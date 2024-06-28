#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(dirname "$SCRIPT_DIR")/

source "$SCRIPT_DIR/load_env_config.sh"

if [ -z $ENV ]; then
    echo "ENV is not set"
    exit 1
fi
echo "ENV is set to $ENV"

if [ -z $EXTERNAL_DIRS_NEEDED ]; then
    echo "EXTERNAL_DIRS_NEEDED is not set"
    exit 1
fi

if [ $EXTERNAL_DIRS_NEEDED == "true" ]; then
    if [ -z $POOL_DIR ]; then
        echo "POOL_DIR is not set"
        exit 1
    fi

    if [ -z $LOG_DIR ]; then
        echo "LOG_DIR is not set"
        exit 1
    fi
else
    export POOL_DIR=${PROJECT_DIR}$POOL_DEFAULT_INTERNAL_DIR
    export LOG_DIR=${PROJECT_DIR}$LOG_DEFAULT_INTERNAL_DIR
    echo "Setting POOL_DIR to $POOL_DIR"
    echo "Setting LOG_DIR to $LOG_DIR"
fi