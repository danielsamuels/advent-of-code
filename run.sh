#!/usr/bin/env bash
set -euo pipefail

YEAR=$(date +%Y)
DAY=$(date +%-d)
DIRNAME="$YEAR/$DAY"

if [[ ! -d "$DIRNAME" ]]; then
  cp -r _template "$DIRNAME"
  exit 0
fi

aoc -r -y "$YEAR" -d "$DAY" "$@"
