#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s --file "<payload.json.gz>"\n' "$(basename "$0")" >&2
}

payload=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --file)
      [[ $# -ge 2 ]] || { usage; exit 2; }
      payload="$2"
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

if [[ -z "$payload" ]]; then
  printf '{"status":"error","code":"missing_file","detail":"--file is required"}\n' >&2
  exit 2
fi

if [[ ! -f "$payload" ]]; then
  printf '{"status":"error","code":"payload_not_found","detail":"file not found: %s"}\n' "$payload" >&2
  exit 1
fi

python3 - <<'PY' "$payload"
import gzip
import hashlib
import json
import sys

path = sys.argv[1]

try:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        obj = json.load(f)
except OSError as e:
    print(json.dumps({"status": "error", "code": "gzip_read_failed", "detail": str(e)}))
    sys.exit(1)
except json.JSONDecodeError as e:
    print(json.dumps({"status": "error", "code": "json_decode_failed", "detail": str(e)}))
    sys.exit(1)

required = ["version", "encoding", "algorithm", "context_sha256", "context_chars", "context"]
missing = [k for k in required if k not in obj]
if missing:
    print(json.dumps({"status": "error", "code": "schema_missing_keys", "detail": ",".join(missing)}))
    sys.exit(1)

if obj["version"] != 1:
    print(json.dumps({"status": "error", "code": "bad_version", "detail": str(obj["version"])}))
    sys.exit(1)

if obj["algorithm"] != "gzip":
    print(json.dumps({"status": "error", "code": "bad_algorithm", "detail": str(obj["algorithm"])}))
    sys.exit(1)

context = obj["context"]
if not isinstance(context, str):
    print(json.dumps({"status": "error", "code": "bad_context_type", "detail": type(context).__name__}))
    sys.exit(1)

actual_chars = len(context.encode("utf-8"))
expected_chars = int(obj["context_chars"])
sha = hashlib.sha256(context.encode("utf-8")).hexdigest()
sha_ok = (sha == obj["context_sha256"])
chars_ok = (actual_chars == expected_chars)

if not sha_ok:
    print(json.dumps({"status": "error", "code": "sha256_mismatch", "expected": obj["context_sha256"], "actual": sha}))
    sys.exit(1)

if not chars_ok:
    print(json.dumps({"status": "error", "code": "char_count_mismatch", "expected": expected_chars, "actual": actual_chars}))
    sys.exit(1)

print(json.dumps({"status": "ok", "sha256_valid": True, "context_chars": actual_chars}))
print("BEGIN_RESTORED_CONTEXT")
print(context)
print("END_RESTORED_CONTEXT")
PY
