#!/bin/bash


# Stop on error
set -e

printenv | grep "APP"

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

# Use existing Python 3.14 (e.g. actions/setup-python) when on PATH so CI does not
# depend on ppa.launchpadcontent.net, which runners sometimes cannot reach.
need_deb_python314=true
if command -v python3.14 >/dev/null 2>&1 \
    && python3.14 -c 'import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 14) else 1)' 2>/dev/null; then
    need_deb_python314=false
fi

apt-get update
if [ "$need_deb_python314" = true ]; then
    DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
    add-apt-repository ppa:deadsnakes/ppa -y
    apt-get update
fi

DEBIAN_FRONTEND=noninteractive apt-get install -y \
    ffmpeg=7:4.4.2-0ubuntu0.22.04.1 \
    tzdata \
    software-properties-common \
    curl \
    jq \
    libchromaprint-tools \
    $([ "$need_deb_python314" = true ] && echo python3.14)

curl https://bootstrap.pypa.io/get-pip.py | python3.14

if [ "$APP_IS_DOCKERIZED" = "true" ]; then
    # Install gosu to run gunicorn as a non root user
    apt-get install -y wget
    wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.12/gosu-amd64"
    chmod +x /usr/local/bin/gosu
fi

# Clean up APT when done.
apt-get clean
rm -rf /var/lib/apt/lists/*

cp env/fpcalc/fpcalc-ubuntu bin/fpcalc
chmod +x bin/fpcalc