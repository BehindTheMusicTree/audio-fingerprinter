FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
    libchromaprint-tools \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT [ "python", "__main__.py" ]
