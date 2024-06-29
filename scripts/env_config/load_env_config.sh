#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
ENV_PATH=$SCRIPT_DIR../../env/.env

if [ -f "$ENV_PATH" ]; then
    echo "Loading environment variables from ${ENV_PATH}..."
    while IFS='=' read -r key value
    do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$ENV_PATH"
else
    echo "$ENV_PATH file does not exist"
fi

if [ -z $ENV ]; then
    echo "ENV is not set"
    exit 1
fi

CONFIG_PATH="$SCRIPT_DIR/../../config/env_config.json"
if [ ! -f "$CONFIG_PATH" ]; then
    echo "Configuration file '${CONFIG_PATH}' was not found."
    exit 1
else
    echo "Loading configuration values from ${CONFIG_PATH}..."
fi

config=$(cat "$CONFIG_PATH")
currentEnvLower=$(echo "$ENV" | tr '[:upper:]' '[:lower:]')

envConfig=$(echo "$config" | jq -r --arg env "$currentEnvLower" '.["environments"][$env]')

internalPaths=$(echo "$config" | jq -r '.["internalPaths"]')

export POOL_DIR=$(echo "$internalPaths" | jq -r '.["pool"]')
export LOG_DIR=$(echo "$internalPaths" | jq -r '.["log"]')