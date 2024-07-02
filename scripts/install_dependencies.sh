#!/bin/bash


# Stop on error
set -e

echo "APP_IS_DOCKERIZED is $APP_IS_DOCKERIZED"
if [ -z $APP_IS_DOCKERIZED ]; then
    echo "APP_IS_DOCKERIZED must be set."
    exit 1
fi
APP_IS_DOCKERIZED=$(echo "$APP_IS_DOCKERIZED" | tr '[:upper:]' '[:lower:]')

if [ $APP_IS_DOCKERIZED != "true" ] && [ $APP_IS_DOCKERIZED != "false" ]; then
    echo "APP_IS_DOCKERIZED must be set to true or false."
    exit 1
fi

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