#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s --input "<context-file>"\n' "$(basename "$0")" >&2
}

input=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input)
      [[ $# -ge 2 ]] || { usage; exit 2; }
      input="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf '{"status":"error","code":"bad_arg","detail":"unknown argument: %s"}\n' "$1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$input" ]]; then
  printf '{"status":"error","code":"missing_input","detail":"--input is required"}\n' >&2
  exit 2
fi

if [[ ! -f "$input" ]]; then
  printf '{"status":"error","code":"input_not_found","detail":"file not found: %s"}\n' "$input" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  printf '{"status":"error","code":"missing_dep","detail":"python3 not found"}\n' >&2
  exit 1
fi

if ! command -v gzip >/dev/null 2>&1; then
  printf '{"status":"error","code":"missing_dep","detail":"gzip not found"}\n' >&2
  exit 1
fi

if command -v sha256sum >/dev/null 2>&1; then
  hash_cmd='sha256sum'
elif command -v shasum >/dev/null 2>&1; then
  hash_cmd='shasum -a 256'
else
  printf '{"status":"error","code":"missing_dep","detail":"sha256 tool not found"}\n' >&2
  exit 1
fi

context_chars=$(wc -c < "$input" | tr -d ' ')
if [[ "$hash_cmd" == 'sha256sum' ]]; then
  context_sha256=$(sha256sum "$input" | awk '{print $1}')
else
  context_sha256=$(shasum -a 256 "$input" | awk '{print $1}')
fi

tmpfile=$(mktemp "/tmp/squash-context-XXXXXX.json")
gzfile="${tmpfile}.gz"

escaped_context=$(python3 - <<'PY' "$input"
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    print(json.dumps(f.read(), ensure_ascii=False))
PY
)

cat > "$tmpfile" <<EOF
{"version":1,"encoding":"utf-8","algorithm":"gzip","context_sha256":"${context_sha256}","context_chars":${context_chars},"context":${escaped_context}}
EOF

gzip -c "$tmpfile" > "$gzfile"
rm -f "$tmpfile"

prompt="In new session run: bash skills/experimental/squash/scripts/squash-unpack.sh --file \"${gzfile}\". Then paste block between BEGIN_RESTORED_CONTEXT and END_RESTORED_CONTEXT as first message."

printf '{"status":"ok","payload_path":"%s","context_sha256":"%s","context_chars":%s,"new_session_prompt":%s}\n' \
  "$gzfile" "$context_sha256" "$context_chars" "$(python3 - <<'PY' "$prompt"
import json,sys
print(json.dumps(sys.argv[1], ensure_ascii=False))
PY
)"
