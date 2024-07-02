#!/bin/bash

required_vars=("APP_IS_DOCKERIZED")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Environment variable $var is not set. Exiting."
        exit 1
    fi
done

# Stop on error
set -e

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
    ffmpeg=7:4.4.2-0ubuntu0.22.04.1 \
    tzdata \
    software-properties-common \
    curl \
    jq \
    python3.12 \
    libchromaprint-tools \
    python3.12-distutils

curl https://bootstrap.pypa.io/get-pip.py | python3.12

if [ "$APP_IS_DOCKERIZED" = "true" ]; then
    # Install gosu to run gunicorn as a non root user
    add-apt-repository ppa:deadsnakes/ppa
    apt-get update
    apt-get install -y wget
    wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.12/gosu-amd64"
    chmod +x /usr/local/bin/gosu
fi

# Clean up APT when done.
apt-get clean
rm -rf /var/lib/apt/lists/*

cp env/fpcalc/fpcalc-ubuntu bin/fpcalc
chmod +x bin/fpcalc