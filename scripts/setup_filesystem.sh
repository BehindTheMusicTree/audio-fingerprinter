#!/bin/bash

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
source "${SCRIPTS_DIR}/env_config/set_env_from_config.sh"

if [ ! -d "$POOL_DIR" ]; then
    echo "Creating pool directory..."
    sudo mkdir -p "$POOL_DIR"
fi

POOL_SYMLINK_TARGET=$AUDIO_FINGERPRINTER_POOL_SYMLINK_TARGET
if [ -n "$POOL_SYMLINK_TARGET" ]; then
    echo "POOL_SYMLINK_TARGET is set to $POOL_SYMLINK_TARGET"
    if [ ! -L "$POOL_SYMLINK_TARGET" ]; then
        echo "Creating symlink for pool directory..."
        sudo ln -s "$POOL_DIR" "$POOL_SYMLINK_TARGET"
    fi
else
    echo "POOL_SYMLINK_TARGET is not set"
fi

if [ ! -d "$LOG_DIR" ]; then
    echo "Creating log directory..."
    sudo mkdir -p "$LOG_DIR"
fi

LOG_SYMLINK_TARGET=$AUDIO_FINGERPRINTER_LOG_SYMLINK_TARGET
if [ -n "$LOG_SYMLINK_TARGET" ]; then
    echo "LOG_SYMLINK_TARGET is set to $LOG_SYMLINK_TARGET"
    if [ ! -L "$LOG_SYMLINK_TARGET" ]; then
        echo "Creating symlink for log directory..."
        sudo ln -s "$LOG_DIR" "$LOG_SYMLINK_TARGET"
    fi
else
    echo "LOG_SYMLINK_TARGET is not set"
fi

sudo chmod 775 "$POOL_DIR" "$LOG_DIR"
sudo chown -R $USER "$POOL_DIR" "$LOG_DIR"