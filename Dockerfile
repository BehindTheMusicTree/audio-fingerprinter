FROM ubuntu:22.04

WORKDIR /app

ARG port

ENV PORT=$port
ENV ENV=TEST

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata && \
    apt-get install -y software-properties-common curl && \ 
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.12 libchromaprint-tools ffmpeg python3.12-distutils && \
    curl https://bootstrap.pypa.io/get-pip.py | python3.12 && \
    rm -rf /var/lib/apt/lists/*

COPY . .

ENV AudioFingerPrintGeneratorPoolDir=/tmp/audio-fingerprint-generator/pool/

RUN python3.12 -m pip install --no-cache-dir --ignore-installed -r requirements.txt

RUN cp env/fpcalc/fpcalc-ubuntu bin/fpcalc && \
    chmod +x bin/fpcalc && \
    mkdir -p ${AudioFingerPrintGeneratorPoolDir} && \
    chmod -R 777 ${AudioFingerPrintGeneratorPoolDir}

ENV PATH="/app/bin:${PATH}"

EXPOSE $PORT

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run"]