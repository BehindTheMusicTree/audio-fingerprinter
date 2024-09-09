#!/bin/bash

echo "Generating calculated paths env file"

# Function to check if a variable is set
check_var() {
    local var_name="$1"
    local var_value="$2"
    if [ -z "$var_value" ]; then
        echo "Error: $var_name must be set" >&2
        exit 1
    fi
}

# Function to convert a variable to lowercase
to_lowercase() {
    echo "$1" | tr '[:upper:]' '[:lower:]'
}

# Function to validate boolean variable
validate_boolean() {
    local var_name="$1"
    local var_value="$2"
    if [ "$var_value" != "true" ] && [ "$var_value" != "false" ]; then
        echo "Error: $var_name must be set to true or false" >&2
        exit 1
    fi
}

# Function to create or clear the generated paths env file
create_env_file() {
    local file_path="$1"
    if [ -f "$file_path" ]; then
        rm -f "$file_path"
    fi
    touch "$file_path"
}

# Main script logic
main() {

    if [ -z "$1" ]; then
        echo "Error: no base dir provided." >&2
        exit 1
    fi
    BASE_DIR=$1
    echo "BASE_DIR: $BASE_DIR"

    if [ -z "$2" ]; then
        echo "Error: no calculated paths env file path provided." >&2
        exit 1
    fi
    GENERATED_PATHS_ENV_FILE=$2
    echo "GENERATED_PATHS_ENV_FILE: $GENERATED_PATHS_ENV_FILE"

    create_env_file "$GENERATED_PATHS_ENV_FILE"

    check_var "FLASK_LOGS_ARE_NEEDED" "$FLASK_LOGS_ARE_NEEDED"
    FLASK_LOGS_ARE_NEEDED=$(to_lowercase "$FLASK_LOGS_ARE_NEEDED")
    validate_boolean "FLASK_LOGS_ARE_NEEDED" "$FLASK_LOGS_ARE_NEEDED"

    if [ "$FLASK_LOGS_ARE_NEEDED" = "true" ]; then
        check_var "APP_IS_EXPOSED" "$APP_IS_EXPOSED"
        APP_IS_EXPOSED=$(to_lowercase "$APP_IS_EXPOSED")
        validate_boolean "APP_IS_EXPOSED" "$APP_IS_EXPOSED"

        if [ "$APP_IS_EXPOSED" = "true" ]; then
            echo "APP_IS_EXPOSED is set to true"
            check_var "DOCKERRIZED_FLASK_LOG_DIR" "$DOCKERRIZED_FLASK_LOG_DIR"
            FLASK_LOG_DIR=${DOCKERRIZED_FLASK_LOG_DIR}
        else
            echo "APP_IS_EXPOSED is set to false"
            check_var "FLASK_LOG_INTERNAL_DIR" "$FLASK_LOG_INTERNAL_DIR"
            FLASK_LOG_DIR=${BASE_DIR}${FLASK_LOG_INTERNAL_DIR}
        fi

        echo "FLASK_LOG_DIR: $FLASK_LOG_DIR"
        echo "FLASK_LOG_DIR=$FLASK_LOG_DIR" >> "$GENERATED_PATHS_ENV_FILE"
    fi

    if [ "$APP_IS_EXPOSED" = "true" ]; then
        echo "APP_IS_EXPOSED is set to true"
        check_var "DOCKERIZED_POOL_DIR" "$DOCKERIZED_POOL_DIR"
        POOL_DIR=${DOCKERIZED_POOL_DIR}
    else
        echo "APP_IS_EXPOSED is set to false"
        check_var "POOL_INTERNAL_DIR" "$POOL_INTERNAL_DIR"
        POOL_DIR=${BASE_DIR}${POOL_INTERNAL_DIR}
    fi

    echo "POOL_DIR: $POOL_DIR"
    echo "POOL_DIR=$POOL_DIR" >> "$GENERATED_PATHS_ENV_FILE"
}

main "$@"