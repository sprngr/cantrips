#!/usr/bin/env bash
# import-plan.sh — validate + extract .skill-plan.yaml for agent resume
# Usage: ./import-plan.sh <path-to-.skill-plan.yaml>
# Exit: 0=ok, 1=missing file, 2=bad yaml, 3=missing keys, 4=already completed

set -euo pipefail

PLAN="$1"

if [ ! -f "$PLAN" ] || [ ! -r "$PLAN" ]; then
  echo "ERROR: file missing or unreadable: $PLAN" >&2
  exit 1
fi

exec python3 - "$PLAN" <<'PYEOF'
import sys, os, json
from datetime import datetime

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not available", file=sys.stderr)
    sys.exit(2)

plan_path = sys.argv[1]

try:
    with open(plan_path, "r") as f:
        data = yaml.safe_load(f)
except Exception as e:
    print(f"ERROR: bad YAML: {e}", file=sys.stderr)
    sys.exit(2)

if not isinstance(data, dict):
    print("ERROR: top-level YAML must be a mapping", file=sys.stderr)
    sys.exit(2)

required = ["intent", "scope", "turns"]
missing = [k for k in required if k not in data]
if missing:
    print(f"WARNING: missing keys: {', '.join(missing)}", file=sys.stderr)
    sys.exit(3)

if data.get("completed") is True:
    print("COMPLETED=true")
    sys.exit(4)

turns = data.get("turns", [])
if isinstance(turns, list):
    turn_count = len(turns)
else:
    turn_count = 0

print(f"INTENT={data['intent']}")
print(f"SCOPE={data.get('scope', 'unknown')}")
print(f"MECHANISM={data.get('mechanism', 'reasoning')}")
print(f"CONTEXT_ASSETS={data.get('context_assets', 'none')}")
print(f"TIER={data.get('tier', 'A')}")
print(f"TARGET_PATH={data.get('target_path', '')}")
print(f"TURNS={turn_count}")
print(f"COMPLETED={str(data.get('completed', False)).lower()}")
if data.get("workflow_notes"):
    notes = "; ".join(data["workflow_notes"])
    print(f"WORKFLOW_NOTES={notes}")
PYEOF
