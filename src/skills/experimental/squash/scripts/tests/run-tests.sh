#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python_bin="${PYTHON_BIN:-}"
if [[ -z "$python_bin" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    python_bin="python3"
  elif command -v python >/dev/null 2>&1; then
    python_bin="python"
  else
    printf 'Error: python runtime not found. Install python3.\n' >&2
    exit 2
  fi
fi

"$python_bin" -m unittest "$script_dir/test_strip_filler.py" "$script_dir/test_squash_session.py"
