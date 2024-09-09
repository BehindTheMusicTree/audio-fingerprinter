#!/bin/bash

echo "Setting up filesystem"

if [ -z "$1" ]; then
    echo "No env file specified"
else
    APP_ENV_FILE="$1"
    if [ ! -f "$APP_ENV_FILE" ]; then
        echo "env file $APP_ENV_FILE does not exist" >&2
        exit 1
    fi
        
    echo "Loading environment variables from ${APP_ENV_FILE}"
    while IFS='=' read -r key value
    do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$APP_ENV_FILE"
fi

scripts_dir=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
project_dir=$(cd "$(dirname "$scripts_dir")" && pwd)/
calculated_paths_env_file=${project_dir}env/calculated_paths/.env
bash "${scripts_dir}generate_calculated_paths_env_file.sh" "$project_dir" "$calculated_paths_env_file"

if [ $? -ne 0 ]; then
    echo "Failed to generate calculated paths env file"
    exit 1
fi

echo "Loading calculated paths from ${calculated_paths_env_file}"
while IFS='=' read -r key value
do
    export "$key=$value"
done < "$calculated_paths_env_file"

required_vars=(
  APP_IS_EXPOSED
  POOL_INTERNAL_DIR
  FLASK_LOGS_ARE_NEEDED
)
for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "$var must be set."
    exit 1
  fi
done

pool_dir=${project_dir}${POOL_INTERNAL_DIR}
echo "pool_dir: $pool_dir"
if [ ! -d "$pool_dir" ]; then
    echo "Creating pool directory $pool_dir"
    mkdir -p "$pool_dir"
fi

echo "FLASK_LOG_DIR: $FLASK_LOG_DIR"
if [ ! -d "$FLASK_LOG_DIR" ]; then
    echo "Creating flask log directory."
    mkdir -p "$FLASK_LOG_DIR"
else
    echo "Flask log directory already exists."
fi

if [ $FLASK_LOGS_ARE_NEEDED = "true" ]; then
    required_vars=(
        FLASK_LOG_DIR
        FLASK_LOG_APP_FILENAME
        FLASK_LOG_ERROR_FILENAME
        FLASK_LOG_REQUESTS_FILENAME
    )
    for var_name in "${required_vars[@]}"; do
        if [ -z "${!var_name}" ]; then
            echo "$var_name must be set as flask logs are needed" >&2
            exit 1
        fi
    done

    FLASK_LOG_APP_FILE=${FLASK_LOG_DIR}${FLASK_LOG_APP_FILENAME}
    echo "FLASK_LOG_APP_FILE: $FLASK_LOG_APP_FILE"
    if [ ! -f "$FLASK_LOG_APP_FILE" ]; then
        echo "Flask log app file does not exist. Creating."
        touch "$FLASK_LOG_APP_FILE"
    else
        echo "Flask log app file already exists."
    fi

    FLASK_LOG_ERROR_FILE=${FLASK_LOG_DIR}${FLASK_LOG_ERROR_FILENAME}
    echo "FLASK_LOG_ERROR_FILE: $FLASK_LOG_ERROR_FILE"
    if [ ! -f "$FLASK_LOG_ERROR_FILE" ]; then
        echo "Flask log error file does not exist. Creating."
        touch "$FLASK_LOG_ERROR_FILE"
    else
        echo "Flask log error file already exists."
    fi

    FLASK_LOG_REQUESTS_FILE=${FLASK_LOG_DIR}${FLASK_LOG_REQUESTS_FILENAME}
    echo "FLASK_LOG_REQUESTS_FILE: $FLASK_LOG_REQUESTS_FILE"
    if [ ! -f "$FLASK_LOG_REQUESTS_FILE" ]; then
        echo "Flask log requests file does not exist. Creating."
        touch "$FLASK_LOG_REQUESTS_FILE"
    else
        echo "Flask log requests file already exists."
    fi
    chmod 775 "$FLASK_LOG_DIR"
else
    echo "Flask logs are not needed."
fi

if [ $APP_IS_EXPOSED = "true" ]; then
    required_vars=(
        GUNICORN_LOG_DIR
        GUNICORN_LOG_ERROR_FILENAME
        GUNICORN_LOG_ACCESS_FILENAME
        POOL_DIR_SYMLINK_TARGET
        FLASK_LOG_DIR_SYMLINK_TARGET
        GUNICORN_LOG_DIR_SYMLINK_TARGET
    )
    for var_name in "${required_vars[@]}"; do
        if [ -z "${!var_name}" ]; then
            echo "$var_name must be set as app is exposed" >&2
            exit 1
        fi
    done

    gunicorn_log_error_file=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ERROR_FILENAME}
    echo "gunicorn_log_error_file: $gunicorn_log_error_file"
    gunicorn_log_access_file=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ACCESS_FILENAME}
    echo "gunicorn_log_access_file: $gunicorn_log_access_file"

    touch "$gunicorn_log_error_file" "$gunicorn_log_access_file"
    chmod -R 775 "$GUNICORN_LOG_DIR"

    echo "POOL_DIR_SYMLINK_TARGET is set to $POOL_DIR_SYMLINK_TARGET"
    if [ ! -L "$POOL_DIR_SYMLINK_TARGET" ]; then
        echo "Creating symlink for pool directory."
        ln -s "$pool_dir" "$POOL_DIR_SYMLINK_TARGET"
    fi

    echo "FLASK_LOG_DIR_SYMLINK_TARGET is set to $FLASK_LOG_DIR_SYMLINK_TARGET"
    if [ ! -L "$FLASK_LOG_DIR_SYMLINK_TARGET" ]; then
        echo "Creating symlink for flask log directory."
        ln -s "$FLASK_LOG_DIR" "$FLASK_LOG_DIR_SYMLINK_TARGET"
    fi

    echo "GUNICORN_LOG_DIR_SYMLINK_TARGET is set to $GUNICORN_LOG_DIR_SYMLINK_TARGET"
    if [ ! -L "$GUNICORN_LOG_DIR_SYMLINK_TARGET" ]; then
        echo "Creating symlink for gunicorn log directory."
        ln -s "$GUNICORN_LOG_DIR" "$GUNICORN_LOG_DIR_SYMLINK_TARGET"
    fi
fi

chmod 775 "$pool_dir"