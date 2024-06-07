# Image ubuntu:22.04 used for all fingerprints env (except dev) for consistent fingerprint generation
FROM ubuntu:22.04

WORKDIR /app

ARG port

ENV PORT=$port
ENV ENV=TEST

RUN apt-get update && \
    add-apt-repository ppa:deadsnakes/ppa && \  
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata && \
    apt-get install -y software-properties-common curl python3.12 libchromaprint-tools ffmpeg python3.12-distutils && \
    curl https://bootstrap.pypa.io/get-pip.py | python3.12 && \
    rm -rf /var/lib/apt/lists/*

# To run gunicorn as a non-root user without password prompt
RUN apt-get install -y gosu

COPY requirements.txt .
RUN python3.12 -m pip install --no-cache-dir --ignore-installed -r requirements.txt

COPY . .

ENV PoolDir=/tmp/audio-fingerprinter/pool/

RUN cp env/fpcalc/fpcalc-ubuntu bin/fpcalc && \
    chmod +x bin/fpcalc && \
    mkdir -p ${PoolDir} && \
    chmod -R 777 ${PoolDir}

EXPOSE $PORT

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0