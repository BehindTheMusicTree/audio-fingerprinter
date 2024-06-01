FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
    libchromaprint-tools \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pydub acoustid

# Copiez votre script Python dans l'image
COPY . /app
WORKDIR /app

# Exécutez votre script Python lorsque le conteneur est lancé
CMD ["python", "your_script.py"]