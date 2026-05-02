#!/usr/bin/env bash
missing=""
for key in "$@"; do
  eval "val=\$$key"
  if [ -z "$val" ]; then
    missing="${missing}${missing:+ }${key}"
  fi
done
if [ -n "$missing" ]; then
  echo "Missing or empty: $missing"
  exit 1
fi
echo "All required vars and secrets are set."

# Validate that GHCR image name components are lowercase and contain only
# characters valid in a Docker image reference (a-z, 0-9, '.', '_', '-', '/').
for key in GHCR_IMAGE_NAMESPACE AFP_IMAGE_REPO; do
  eval "val=\$$key"
  if [ -n "$val" ] && ! echo "$val" | grep -qE '^[a-z0-9._/-]+$'; then
    echo "Invalid Docker image name format for: ${key}='${val}'. Must contain only lowercase a-z, 0-9, and characters: . _ - /"
    exit 1
  fi
done
