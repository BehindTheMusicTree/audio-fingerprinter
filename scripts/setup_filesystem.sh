#!/bin/bash

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
source "${SCRIPTS_DIR}env_config/set_env_from_config.sh"

if [ ! -d "$POOL_DIR" ]; then
    echo "Creating pool directory..."
    mkdir -p "$POOL_DIR"
fi

if [ -n "$POOL_DIR_SYMLINK_TARGET" ]; then
    echo "POOL_DIR_SYMLINK_TARGET is set to $POOL_DIR_SYMLINK_TARGET"
    if [ ! -L "$POOL_DIR_SYMLINK_TARGET" ]; then
        echo "Creating symlink for pool directory..."
        ln -s "$POOL_DIR" "$POOL_DIR_SYMLINK_TARGET"
    fi
else
    echo "POOL_DIR_SYMLINK_TARGET is not set"
fi

if [ ! -d "$LOG_DIR" ]; then
    echo "Creating log directory..."
    mkdir -p "$LOG_DIR"
fi

if [ -n "$LOG_DIR_SYMLINK_TARGET" ]; then
    echo "LOG_DIR_SYMLINK_TARGET is set to $LOG_DIR_SYMLINK_TARGET"
    if [ ! -L "$LOG_DIR_SYMLINK_TARGET" ]; then
        echo "Creating symlink for log directory..."
        ln -s "$LOG_DIR" "$LOG_DIR_SYMLINK_TARGET"
    fi
else
    echo "LOG_DIR_SYMLINK_TARGET is not set"
fi

chmod 775 "$POOL_DIR" "$LOG_DIR"
chown -R $USER "$POOL_DIR" "$LOG_DIR"