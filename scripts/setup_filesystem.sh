#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
echo "SCRIPT_DIR is set to $SCRIPT_DIR"
source "${SCRIPTS_DIR}/env_config/set_env_from_config.sh"

if [ ! -d "$POOL_DIR" ]; then
    echo "Creating pool directory..."
    sudo mkdir -p $POOL_DIR
fi

if [ ! -d "$LOG_DIR" ]; then
    echo "Creating log directory..."
    sudo mkdir -p $LOG_DIR
fi

sudo chmod 775 $POOL_DIR $LOG_DIR
sudo chown -R $USER $POOL_DIR $LOG_DIR