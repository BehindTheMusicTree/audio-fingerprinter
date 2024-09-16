#!/bin/bash

echo "Generating calculated paths env file"

check_var() {
    local var_name="$1"
    local var_value="$2"
    if [ -z "$var_value" ]; then
        echo "Error: $var_name must be set" >&2
        exit 1
    fi
}

to_lowercase() {
    echo "$1" | tr '[:upper:]' '[:lower:]'
}

validate_boolean() {
    local var_name="$1"
    local var_value="$2"
    if [ "$var_value" != "true" ] && [ "$var_value" != "false" ]; then
        echo "Error: $var_name must be set to true or false" >&2
        exit 1
    fi
}

create_env_file() {
    local file_path="$1"
    if [ -f "$file_path" ]; then
        rm -f "$file_path"
    fi
    touch "$file_path"
}

calculate_flask_log_dir(){
    if [ -n "$FLASK_LOG_DIR_EXTERNAL" ]; then
        if [ -n "$FLASK_LOG_DIR_INTERNAL" ]; then
            echo "FLASK_LOG_DIR_INTERNAL and FLASK_LOG_DIR_EXTERNAL must not be set at the same time." >&2
            exit 1
        fi
        echo "FLASK_LOG_DIR_EXTERNAL is set. Setting the Flask logs to external."
        FLASK_LOG_DIR="${FLASK_LOG_DIR_EXTERNAL}"
    else
        if [ -n "$FLASK_LOG_DIR_INTERNAL" ]; then
            echo "FLASK_LOG_DIR_INTERNAL is set. Setting the Flask logs to internal."
            FLASK_LOG_DIR="${APP_DIR}${FLASK_LOG_DIR_INTERNAL}"
        else
            echo "Neither FLASK_LOG_DIR_EXTERNAL nor FLASK_LOG_DIR_INTERNAL is set. Flask logs are not needed."
        fi
    fi

    if [ -n "$FLASK_LOG_DIR" ]; then
        echo "FLASK_LOG_DIR is set to $FLASK_LOG_DIR"
        echo "FLASK_LOG_DIR=$FLASK_LOG_DIR" >> "$CALCULATED_PATHS_ENV_FILE"
    fi
}

calculate_pool_dir(){
    if [ -n "$POOL_DIR_EXTERNAL" ]; then
        echo "POOL_DIR_EXTERNAL is set. Setting to POOL_DIR."
        if [ -n "$POOL_DIR_INTERNAL" ]; then
            echo "POOL_DIR_INTERNAL and POOL_DIR_EXTERNAL can not be set at the same time." >&2
            exit 1
        fi
        POOL_DIR=${POOL_DIR_EXTERNAL}
    else
        if [ -n "$POOL_DIR_INTERNAL" ]; then
            echo "POOL_DIR_INTERNAL is set. Setting to POOL_DIR."
            POOL_DIR=${PROJECT_DIR}${POOL_DIR_INTERNAL}
        else 
            echo "Neither POOL_DIR_EXTERNAL nor POOL_DIR_INTERNAL is set. Abort." >&2
            exit 1
        fi
    fi

    echo "POOL_DIR: $POOL_DIR"
    echo "POOL_DIR=$POOL_DIR" >> "$CALCULATED_PATHS_ENV_FILE"
}

main() {
    echo "Generating the env file for calculated paths..."

    SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    PROJECT_DIR=$(cd "$(dirname "$SCRIPTS_DIR")" && pwd)/
    CALCULATED_PATHS_ENV_FILE="${PROJECT_DIR}env/calculated_paths/.env"

    touch_file_or_exit "$CALCULATED_PATHS_ENV_FILE"

    calculate_flask_log_dir
    calculate_pool_dir

    echo "Calculated paths env file generated successfully."
}

main "$@"