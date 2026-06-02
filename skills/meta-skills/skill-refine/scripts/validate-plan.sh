#!/usr/bin/env bash
# validate-plan.sh - Validate .skill-plan YAML for skill-forge import contract
# Usage: scripts/validate-plan.sh <path-to-.skill-plan.yaml>
#
# Gate intent:
# - This validator is operational/read-permissive and focused on forge import safety.
# - It intentionally does NOT enforce ADR-0002 strict write contract details
#   (path prefix, workflow_notes canonical type, coverage shape, etc.).
# - For strict write-contract enforcement, use repo root script:
#     python3 scripts/audit-skill-plans.py --fail-on-violation

set -euo pipefail

PLAN="${1:?Usage: validate-plan.sh <path-to-.skill-plan.yaml>}"

if [[ ! -f "$PLAN" ]] || [[ ! -r "$PLAN" ]]; then
  echo "ERROR: file missing or unreadable: $PLAN" >&2
  exit 1
fi

python3 - "$PLAN" <<'PYEOF'
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
    print("ERROR: top-level YAML must be mapping", file=sys.stderr)
    sys.exit(2)

required = ["intent", "scope", "mechanism", "target_path", "tier"]
missing = [k for k in required if k not in data]
if missing:
    print(f"ERROR: missing keys: {', '.join(missing)}", file=sys.stderr)
    sys.exit(3)

if data.get("scope") not in {"single", "moderate", "extended"}:
    print("ERROR: invalid scope", file=sys.stderr)
    sys.exit(3)

if data.get("mechanism") not in {"reasoning", "scripts", "hybrid"}:
    print("ERROR: invalid mechanism", file=sys.stderr)
    sys.exit(3)

if data.get("tier") not in {"A", "B", "C"}:
    print("ERROR: invalid tier", file=sys.stderr)
    sys.exit(3)

target_path = str(data.get("target_path", "")).strip()
if not target_path:
    print("ERROR: missing/empty target_path", file=sys.stderr)
    sys.exit(3)

if data.get("completed") is not True:
    print("ERROR: completed must be true", file=sys.stderr)
    sys.exit(4)

print("VALID=true")
PYEOF
