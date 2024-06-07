# Image ubuntu:22.04 used for all fingerprints env (except dev) for consistent fingerprint generation
FROM ubuntu:22.04

WORKDIR /app

ARG port

ENV PORT=$port
ENV ENV=TEST

# software-properties-common is required for add-apt-repository
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y curl python3.12 libchromaprint-tools ffmpeg python3.12-distutils && \
    curl https://bootstrap.pypa.io/get-pip.py | python3.12 && \
    rm -rf /var/lib/apt/lists/*

# To run gunicorn as a non-root user without password prompt
# Second apt-get update is necessary to take into account the new repositories from add-apt-repository 
# ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y wget && \
wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.12/gosu-amd64" && \
chmod +x /usr/local/bin/gosu

COPY requirements.txt .
RUN python3.12 -m pip install --no-cache-dir --ignore-installed -r requirements.txt

COPY . .

ENV PoolDir=/tmp/audio-fingerprinter/pool/

RUN cp env/fpcalc/fpcalc-ubuntu bin/fpcalc && \
    chmod +x bin/fpcalc && \
    mkdir -p ${PoolDir} && \
    chmod -R 777 ${PoolDir}

EXPOSE $PORT

CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "run:app"]