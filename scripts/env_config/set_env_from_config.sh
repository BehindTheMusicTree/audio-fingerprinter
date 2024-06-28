#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$SCRIPT_DIR../../

source "$SCRIPT_DIR/load_env_config.sh"

if [ -z $ENV ]; then
    echo "ENV is not set"
    exit 1
fi
echo "ENV is set to $ENV"

export LOG_DIR=${PROJECT_DIR}$LOG_DIR
echo "Setting LOG_DIR to $LOG_DIR"

export POOL_DIR=${PROJECT_DIR}$POOL_DIR
echo "Setting POOL_DIR to $POOL_DIR"