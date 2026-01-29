FROM python:3.12-slim

WORKDIR /app

ARG port

ENV PORT=$port
ENV ENV=TEST

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ffmpeg \
        libchromaprint-tools && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

ENV PoolDir=/tmp/audio-fingerprinter/pool/

RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN cp env/fpcalc/fpcalc-ubuntu bin/fpcalc && \
    chmod +x bin/fpcalc && \
    mkdir -p ${PoolDir} && \
    chmod -R 777 ${PoolDir}

ENV PATH="/app/bin:${PATH}"

EXPOSE $PORT

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run"]
