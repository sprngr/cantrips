#!/usr/bin/env bash
set -euo pipefail

if [[ $# -gt 2 ]]; then
  printf 'Usage: %s [output-path] [input-file]\n' "$0" >&2
  exit 64
fi

if [[ $# -ge 1 && -z "$1" ]]; then
  printf 'Error: output-path cannot be empty when provided.\n' >&2
  printf 'Usage: %s [output-path] [input-file]\n' "$0" >&2
  exit 64
fi

output_path="${1:-}"
input_file="${2:-}"

if [[ -n "$input_file" && ! -f "$input_file" ]]; then
  printf 'Error: input-file not found: %s\n' "$input_file" >&2
  exit 66
fi

if [[ -z "$output_path" ]]; then
  temp_root="${TMPDIR:-${TEMP:-${TMP:-/tmp}}}"
  mkdir -p "$temp_root"
  stamp="$(date +%Y%m%d-%H%M%S)"
  output_path="$(mktemp "${temp_root%/}/handoff-${stamp}-XXXXXX.md")"
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -n "$input_file" ]]; then
  saved_raw="$("$script_dir/strip-filler.sh" "$input_file" | "$script_dir/write-handoff.sh" "$output_path")"
else
  saved_raw="$("$script_dir/strip-filler.sh" | "$script_dir/write-handoff.sh" "$output_path")"
fi

printf 'saved: %s\n' "$saved_raw"
