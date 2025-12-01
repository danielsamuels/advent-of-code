#!/usr/bin/env bash
set -euo pipefail

YEAR=$(date +%Y)
DAY=$(date +%-d)
DIRNAME="$YEAR/$DAY"

if [[ ! -d "$DIRNAME" ]]; then
  mkdir -p "$DIRNAME"
  cp -r _template/* "$DIRNAME"
  exit 0
fi

if [[ $YEAR -lt 2025 ]]; then

  if [[ ! -d env ]]; then
    python -m venv env
  fi

  if [[ ! -x "$(command -v aoc)" ]]; then
    . env/Scripts/activate
    pip install -r requirements.txt
  fi

  aoc -r -y "$YEAR" -d "$DAY" "$@"

else
  uv run --with "advent-of-code-data>=2.1.0" aoc -r -y "$YEAR" -d "$DAY" "$@"
fi

