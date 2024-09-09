#!/bin/bash

echo "Setting up filesystem"

load_env_file() {
    local env_file="$1"
    if [ ! -f "$env_file" ]; then
        echo "env file $env_file does not exist" >&2
        exit 1
    fi

    echo "Loading environment variables from ${env_file}"
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$env_file"
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

create_directory() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        echo "Creating directory $dir"
        mkdir -p "$dir"
    else
        echo "Directory $dir already exists."
    fi
}

create_log_file() {
    local log_file="$1"
    if [ ! -f "$log_file" ]; then
        echo "Log file $log_file does not exist. Creating."
        touch "$log_file"
    else
        echo "Log file $log_file already exists."
    fi
}

create_symlink() {
    local target="$1"
    local link_name="$2"
    if [ ! -L "$link_name" ]; then
        echo "Creating symlink for $link_name."
        ln -s "$target" "$link_name"
    fi
}

main() {
    if [ -z "$1" ]; then
        echo "No env file specified"
    else
        APP_ENV_FILE="$1"
        load_env_file "$APP_ENV_FILE"
    fi

    scripts_dir=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    project_dir=$(cd "$(dirname "$scripts_dir")" && pwd)/
    calculated_paths_env_file=${project_dir}env/calculated_paths/.env
    bash "${scripts_dir}generate_calculated_paths_env_file.sh" "$project_dir" "$calculated_paths_env_file"

    if [ $? -ne 0 ]; then
        echo "Failed to generate calculated paths env file"
        exit 1
    fi

    load_env_file "$calculated_paths_env_file"

    required_vars=(
        APP_IS_EXPOSED
        POOL_INTERNAL_DIR
        FLASK_LOGS_ARE_NEEDED
    )
    check_required_vars "${required_vars[@]}"

    pool_dir=${project_dir}${POOL_INTERNAL_DIR}
    echo "pool_dir: $pool_dir"
    create_directory "$pool_dir"

    echo "FLASK_LOG_DIR: $FLASK_LOG_DIR"
    create_directory "$FLASK_LOG_DIR"

    echo "FLASK_LOGS_ARE_NEEDED: $FLASK_LOGS_ARE_NEEDED"
    if [ "$FLASK_LOGS_ARE_NEEDED" = "true" ]; then
        required_vars=(
            FLASK_LOG_DIR
            FLASK_LOG_APP_FILENAME
            FLASK_LOG_ERROR_FILENAME
            FLASK_LOG_REQUESTS_FILENAME
        )
        check_required_vars "${required_vars[@]}"

        FLASK_LOG_APP_FILE=${FLASK_LOG_DIR}${FLASK_LOG_APP_FILENAME}
        echo "FLASK_LOG_APP_FILE: $FLASK_LOG_APP_FILE"
        create_log_file "$FLASK_LOG_APP_FILE"

        FLASK_LOG_ERROR_FILE=${FLASK_LOG_DIR}${FLASK_LOG_ERROR_FILENAME}
        echo "FLASK_LOG_ERROR_FILE: $FLASK_LOG_ERROR_FILE"
        create_log_file "$FLASK_LOG_ERROR_FILE"

        FLASK_LOG_REQUESTS_FILE=${FLASK_LOG_DIR}${FLASK_LOG_REQUESTS_FILENAME}
        echo "FLASK_LOG_REQUESTS_FILE: $FLASK_LOG_REQUESTS_FILE"
        create_log_file "$FLASK_LOG_REQUESTS_FILE"

        chmod 775 "$FLASK_LOG_DIR"
    else
        echo "Flask logs are not needed."
    fi

    echo "APP_IS_EXPOSED: $APP_IS_EXPOSED"
    if [ "$APP_IS_EXPOSED" = "true" ]; then
        required_vars=(
            GUNICORN_LOG_DIR
            GUNICORN_LOG_ERROR_FILENAME
            GUNICORN_LOG_ACCESS_FILENAME
            POOL_DIR_SYMLINK_TARGET
            FLASK_LOG_DIR_SYMLINK_TARGET
            GUNICORN_LOG_DIR_SYMLINK_TARGET
        )
        check_required_vars "${required_vars[@]}"

        create_directory "$GUNICORN_LOG_DIR"

        GUNICORN_LOG_ERROR_FILE=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ERROR_FILENAME}
        echo "GUNICORN_LOG_ERROR_FILE: $GUNICORN_LOG_ERROR_FILE"
        GUNICORN_LOG_ACCESS_FILE=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ACCESS_FILENAME}
        echo "GUNICORN_LOG_ACCESS_FILE: $GUNICORN_LOG_ACCESS_FILE"

        touch "$GUNICORN_LOG_ERROR_FILE" "$GUNICORN_LOG_ACCESS_FILE"
        chmod -R 775 "$GUNICORN_LOG_DIR"

        create_symlink "$pool_dir" "$POOL_DIR_SYMLINK_TARGET"
        create_symlink "$FLASK_LOG_DIR" "$FLASK_LOG_DIR_SYMLINK_TARGET"
        create_symlink "$GUNICORN_LOG_DIR" "$GUNICORN_LOG_DIR_SYMLINK_TARGET"
    fi

    chmod 775 "$pool_dir"
}

main "$@"