#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  printf 'Usage: %s <output-path>\n' "$0" >&2
  exit 64
fi

target="$1"
mkdir -p "$(dirname "$target")"

tmp_file="$(mktemp)"
cat > "$tmp_file"
mv "$tmp_file" "$target"

printf '%s\n' "$target"
