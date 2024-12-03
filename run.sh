#!/usr/bin/env bash
set -euo pipefail

YEAR=$(date +%Y)
DAY=$(date +%-d)
DIRNAME="$YEAR/$DAY"

if [[ ! -d "$DIRNAME" ]]; then
  cp -r _template "$DIRNAME"
fi

aoc -r -y "$YEAR" -d "$DAY" "$@"
