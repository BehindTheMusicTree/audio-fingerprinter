FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata && \
    apt-get install -y software-properties-common && \ 
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.12 python3-pip libchromaprint-tools ffmpeg python3.12-distutils && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN python3.12 -m pip install pip==21.2.4 && \
    python3.12 -m pip install --no-cache-dir -r requirements.txt

RUN cp env/fpcalc/fpcalc-ubuntu bin/fpcalc && \
    chmod +x bin/fpcalc && \
    cp env/variables/test/.env .env

ENV PATH="/app/bin:${PATH}"

ENTRYPOINT [ "python3.12", "__main__.py" ]