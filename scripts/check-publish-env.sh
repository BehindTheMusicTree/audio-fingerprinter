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
