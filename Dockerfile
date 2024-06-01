FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

RUN ls && \
    apt update && \
    apt install -y libchromaprint-tools ffmpeg && \
    rm -rf /var/lib/apt/lists/* && \
    cp env/fpcalc/fpcalc-ubuntu bin/fpcalc && \
    chmod +x bin/fpcalc && \
    cp env/variables/test/.env .env && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV PATH="/app/bin:${PATH}"

ENTRYPOINT [ "python", "__main__.py" ]