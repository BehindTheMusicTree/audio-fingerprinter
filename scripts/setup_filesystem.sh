#!/bin/bash

echo "Setting up filesystem"

load_app_env_file_if_exists() {
    local SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    local APP_DIR=$(realpath "${SCRIPTS_DIR}..")/
    local ENV_FILE=${APP_DIR}env/.env
    if [ ! -f "$ENV_FILE" ]; then
        echo "$ENV_FILE env file does not exist."
    else
        echo "Loading environment variables from ${ENV_FILE} ..."
        while IFS='=' read -r key value; do
            # Skip comments and empty lines
            if [ -z "$key" ]; then continue; fi
            export "$key=$value"
        done < "$ENV_FILE"
    fi
}

load_app_calculated_paths_env_vars() {
    echo "Loading calculated paths..."
    local SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    local APP_DIR=$(realpath "${SCRIPTS_DIR}..")/
    local CALTULATED_PATHS_DIR="${APP_DIR}env/calculated_paths/"

    if [ ! -d "$CALTULATED_PATHS_DIR" ]; then
        echo "$CALTULATED_PATHS_DIR directory does not exist" >&2
        exit 1
    fi

    local CALCULATED_PATHS_ENV_FILE="${CALTULATED_PATHS_DIR}.env"
    bash "${SCRIPTS_DIR}generate_calculated_paths_env_file.sh"
    if [ $? -ne 0 ]; then
        echo "Failed to generate calculated paths env file: $output" >&2
        exit 1
    fi
    
    echo "Loading calculated paths from ${CALCULATED_PATHS_ENV_FILE}"
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$CALCULATED_PATHS_ENV_FILE"
    echo "Calculated paths loaded successfully."
}

check_required_vars() {
    local required_vars=("$@")
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            echo "$var must be set."
            exit 1
        fi
    done
}

create_directory_if_not_exists_or_exit() {
    local dir_path=$1
    if [ ! -d "$dir_path" ]; then
        echo "Creating directory $dir_path ..."
        output=$(mkdir -p "$dir_path")
        if [ $? -ne 0 ]; then
            echo "Failed to create directory $dir_path : $output" >&2
            exit 1
        fi
        echo "Directory $dir_path created successfully."
        
    else
        echo "Directory $dir_path already exists"
    fi
}

set_read_write_permissions_and_owner_or_exit() {
    local path=$1
    local user=$(whoami)
    output=$(chmod -R 740 "$path")
    if [ $? -ne 0 ]; then
        echo "Failed to change permissions of $path : $output" >&2
        exit 1
    fi
    output=$(chown -R "$user" "$path")
    if [ $? -ne 0 ]; then
        echo "Failed to change owner of $path : $output" >&2
        exit 1
    fi
}

touch_file_or_exit() {
    local file_path=$1
    echo "Touching file $file_path ..."
    output=$(touch "$file_path")
    if [ $? -ne 0 ]; then
        echo "Failed to create file $file_path : $output" >&2
        exit 1
    fi
    echo "File $file_path created successfully."
}

main() {
    SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    PROJECT_DIR=$(cd "$(dirname "$SCRIPTS_DIR")" && pwd)/
    APP_ENV_FILE="${PROJECT_DIR}env/.env"
    source "${SCRIPTS_DIR}utils.sh"
    
    load_app_env_file_if_exists
    load_app_calculated_paths_env_vars

    check_required_vars_are_set POOL_DIR
    check_bool_vars_are_set APP_IS_EXPOSED

    create_directory_if_not_exists_or_exit "$POOL_DIR"
    set_read_write_permissions_and_owner_or_exit "$POOL_DIR"

    if [ -n "${FLASK_LOG_DIR}" ]; then
        echo "A flask log directory is set. Setting up Flask logs..."
        local REQUIRED_VARS=(
            FLASK_LOG_DIR
            FLASK_LOG_APP_FILENAME
            FLASK_LOG_ERROR_FILENAME
            FLASK_LOG_REQUESTS_FILENAME
        )
        check_required_vars_are_set "${REQUIRED_VARS[@]}"

        create_directory_if_not_exists_or_exit "$FLASK_LOG_DIR"
        touch_file_or_exit "${FLASK_LOG_DIR}${FLASK_LOG_APP_FILENAME}"
        touch_file_or_exit "${FLASK_LOG_DIR}${FLASK_LOG_ERROR_FILENAME}"
        touch_file_or_exit "${FLASK_LOG_DIR}${FLASK_LOG_REQUESTS_FILENAME}"
        set_read_write_permissions_and_owner_or_exit "$FLASK_LOG_DIR"

        echo "Flask logs set up successfully."
    else
        echo "Flask logs are not needed."
    fi

    if [ "$APP_IS_EXPOSED" = "true" ]; then
        echo "App is exposed. Setting up gunicorn logs..."
        REQUIRED_VARS=(
            GUNICORN_LOG_DIR
            GUNICORN_LOG_ERROR_FILENAME
            GUNICORN_LOG_ACCESS_FILENAME
        )
        check_required_vars_are_set "${REQUIRED_VARS[@]}"

        create_directory_if_not_exists_or_exit "$GUNICORN_LOG_DIR"
        touch_file_or_exit "${GUNICORN_LOG_DIR}${GUNICORN_LOG_ERROR_FILENAME}"
        touch_file_or_exit "${GUNICORN_LOG_DIR}${GUNICORN_LOG_ACCESS_FILENAME}"
        set_read_write_permissions_and_owner_or_exit "$GUNICORN_LOG_DIR"

        echo "Gunicorn logs set up successfully."
    fi
    echo "Filesystem setup completed successfully."
}

main "$@"