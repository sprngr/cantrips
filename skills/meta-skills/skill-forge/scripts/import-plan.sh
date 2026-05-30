#!/usr/bin/env bash
# import-plan.sh — validate + extract completed .skill-plan.yaml for generation
# Requires: python3, PyYAML
# Usage: ./import-plan.sh <path-to-.skill-plan.yaml>
# Output: JSON object with normalized plan fields
# Exit: 0=ok, 1=usage/missing file, 2=bad yaml, 3=missing/invalid keys, 4=incomplete plan

set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <path-to-.skill-plan.yaml>" >&2
  exit 1
fi

PLAN="$1"

if [ ! -f "$PLAN" ] || [ ! -r "$PLAN" ]; then
  echo "ERROR: file missing or unreadable: $PLAN" >&2
  exit 1
fi

exec python3 - "$PLAN" <<'PYEOF'
import json
import sys

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not available", file=sys.stderr)
    sys.exit(2)

plan_path = sys.argv[1]

try:
    with open(plan_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
except Exception as e:
    print(f"ERROR: bad YAML: {e}", file=sys.stderr)
    sys.exit(2)

if not isinstance(data, dict):
    print("ERROR: top-level YAML must be a mapping", file=sys.stderr)
    sys.exit(2)

required = ["intent", "scope", "mechanism", "target_path", "tier"]
missing = [k for k in required if k not in data]
if missing:
    print(f"WARNING: missing keys: {', '.join(missing)}", file=sys.stderr)
    sys.exit(3)

scope = data.get("scope")
if scope not in {"single", "moderate", "extended"}:
    print(f"WARNING: invalid scope '{scope}' (expected single|moderate|extended)", file=sys.stderr)
    sys.exit(3)

mechanism = data.get("mechanism")
if mechanism not in {"reasoning", "scripts", "hybrid"}:
    print(f"WARNING: invalid mechanism '{mechanism}' (expected reasoning|scripts|hybrid)", file=sys.stderr)
    sys.exit(3)

tier = data.get("tier")
if tier not in {"A", "B", "C"}:
    print(f"WARNING: invalid tier '{tier}' (expected A|B|C)", file=sys.stderr)
    sys.exit(3)

target_path = str(data.get("target_path", "")).strip()
if not target_path:
    print("WARNING: missing/empty target_path", file=sys.stderr)
    sys.exit(3)

if data.get("completed") is not True:
    print("WARNING: plan incomplete; completed must be true", file=sys.stderr)
    sys.exit(4)

turns = data.get("turns", [])
if isinstance(turns, list):
    turn_count = len(turns)
elif isinstance(turns, int):
    turn_count = turns
else:
    turn_count = 0

context_assets = data.get("context_assets", "none")
if isinstance(context_assets, list):
    context_assets_out = ",".join(str(v) for v in context_assets)
elif isinstance(context_assets, dict):
    context_assets_out = ";".join(f"{k}:{v}" for k, v in context_assets.items())
elif context_assets is None:
    context_assets_out = "none"
else:
    context_assets_out = str(context_assets)

workflow_notes = data.get("workflow_notes")
if isinstance(workflow_notes, list):
    notes = "; ".join(str(n) for n in workflow_notes)
elif isinstance(workflow_notes, dict):
    parts = []
    for k, v in workflow_notes.items():
        if isinstance(v, list):
            v_str = " | ".join(str(item) for item in v)
        elif isinstance(v, dict):
            v_str = ", ".join(f"{ik}:{iv}" for ik, iv in v.items())
        else:
            v_str = str(v)
        parts.append(f"{k}={v_str}")
    notes = "; ".join(parts)
elif workflow_notes is None:
    notes = ""
else:
    notes = str(workflow_notes)

payload = {
    "intent": data["intent"],
    "scope": scope,
    "mechanism": mechanism,
    "context_assets": context_assets_out,
    "tier": tier,
    "target_path": target_path,
    "turns": turn_count,
    "completed": True,
}
if notes:
    payload["workflow_notes"] = notes

print(json.dumps(payload, ensure_ascii=False))
PYEOF
