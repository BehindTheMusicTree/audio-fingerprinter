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

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(cd "$(dirname "$SCRIPTS_DIR")" && pwd)/
CALCULATED_PATHS_ENV_FILE=${PROJECT_DIR}env/calculated_paths/.env
bash "${SCRIPTS_DIR}generate_calculated_paths_env_file.sh" "$PROJECT_DIR" "$CALCULATED_PATHS_ENV_FILE"

if [ $? -ne 0 ]; then
    echo "Failed to generate calculated paths env file"
    exit 1
fi

echo "Loading calculated paths from ${CALCULATED_PATHS_ENV_FILE}"
while IFS='=' read -r key value
do
    export "$key=$value"
done < "$CALCULATED_PATHS_ENV_FILE"

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

POOL_DIR=${PROJECT_DIR}${POOL_INTERNAL_DIR}
echo "POOL_DIR: $POOL_DIR"
if [ ! -d "$POOL_DIR" ]; then
    echo "Creating pool directory."
    mkdir -p "$POOL_DIR"
fi

if [ ! -d "$FLASK_LOG_DIR" ]; then
    echo "Creating flask log directory."
    mkdir -p "$FLASK_LOG_DIR"
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

    GUNICORN_LOG_ERROR_FILE=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ERROR_FILENAME}
    echo "GUNICORN_LOG_ERROR_FILE: $GUNICORN_LOG_ERROR_FILE"
    GUNICORN_LOG_ACCESS_FILE=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ACCESS_FILENAME}
    echo "GUNICORN_LOG_ACCESS_FILE: $GUNICORN_LOG_ACCESS_FILE"
    touch "$GUNICORN_LOG_ERROR_FILE" "$GUNICORN_LOG_ACCESS_FILE"
    chmod -R 775 "$GUNICORN_LOG_DIR"

    echo "POOL_DIR_SYMLINK_TARGET is set to $POOL_DIR_SYMLINK_TARGET"
    if [ ! -L "$POOL_DIR_SYMLINK_TARGET" ]; then
        echo "Creating symlink for pool directory."
        ln -s "$POOL_DIR" "$POOL_DIR_SYMLINK_TARGET"
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

chmod 775 "$POOL_DIR"