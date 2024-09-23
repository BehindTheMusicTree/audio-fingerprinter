#!/bin/bash

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

touch_file_or_exit() {
    local file_path=$1
    echo "Creating file $file_path ..."
    output=$(touch "$file_path")
    if [ $? -ne 0 ]; then
        echo "Failed to create file $file_path : $output" >&2
        exit 1
    fi
    echo "File $file_path created successfully."
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

check_required_vars_are_set() {
    local missing_vars=()
    for var_name in "$@"; do
        if [ -z "${!var_name}" ]; then
            echo "$var_name is not set" >&2
            exit 1
        fi
    done
}

check_bool_vars_are_set() {
    local invalid_vars=()
    for var_name in "$@"; do
        if [ -z "${!var_name}" ]; then
            echo "$var_name is not set" >&2
            invalid_vars+=("$var_name")
        elif [ "${!var_name}" != "true" ] && [ "${!var_name}" != "false" ]; then
            echo "$var_name is not a valid boolean (true/false)" >&2
            invalid_vars+=("$var_name")
        fi
    done

    if [ ${#invalid_vars[@]} -ne 0 ]; then
        echo "The following boolean variables are invalid: ${invalid_vars[*]}" >&2
        exit 1
    fi
}

export_value_removing_eventual_surrounding_quotes() {
    local VAR_NAME=$1
    local VAR_VALUE=${!VAR_NAME}
    VAR_VALUE=${VAR_VALUE#\'}
    VAR_VALUE=${VAR_VALUE%\'}
    export "$VAR_NAME=$VAR_VALUE"
}