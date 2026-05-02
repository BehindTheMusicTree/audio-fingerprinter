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
invalid=""
for key in GHCR_IMAGE_NAMESPACE AFP_IMAGE_REPO; do
  eval "val=\$$key"
  if [ -n "$val" ] && ! echo "$val" | grep -qE '^[a-z0-9._/-]+$'; then
    invalid="${invalid}${invalid:+ }${key}"
  fi
done
if [ -n "$invalid" ]; then
  echo "Docker image name must be lowercase and contain only a-z, 0-9, '.', '_', '-', '/': $invalid"
  exit 1
fi
