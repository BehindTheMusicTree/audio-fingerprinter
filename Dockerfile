FROM ubuntu:22.04

WORKDIR /app

ARG port

ENV PORT=$port

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata && \
    apt-get install -y software-properties-common curl && \ 
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.12 libchromaprint-tools ffmpeg python3.12-distutils && \
    curl https://bootstrap.pypa.io/get-pip.py | python3.12 && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN python3.12 -m install --no-cache-dir --ignore-installed -r requirements.txt

RUN cp env/fpcalc/fpcalc-ubuntu bin/fpcalc && \
    chmod +x bin/fpcalc && \
    cp env/variables/test/.env .env

ENV PATH="/app/bin:${PATH}"

EXPOSE 8000

ENTRYPOINT [ "python3.12", "__main__.py" ]