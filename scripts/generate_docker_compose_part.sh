SCRPIT_DIR=$(dirname $0)/

cat << EOF > ${SCRPIT_DIR}$DOCKER_COMPOSE_PART_FILENAME
  audio_fingerprinter:
    working_dir: /app/
    image: $DOCKERHUB_USERNAME/$IMAGE_REPO:$IMAGE_TAG
    container_name: $CONTAINER_NAME
    volumes:
      - api-upload-temp-files:/tmp/bodzify-audio-fingerprinter/pool/
      - afg-log-dir:/var/log/bodzify-audio-fingerprinter/
    ports:
      - "$APP_PORT:$APP_PORT"
    networks:
      - bodzify-network
    env_file: $ENV_VARIABLES_FILENAME
EOF