#!/usr/bin/env bash
# compare-structure.sh - Compare skill directory structure against skills-ref patterns
# Requires: jq
# Usage: scripts/compare-structure.sh <skill-path>
# Output: JSON with structure_score, expected_dirs, found_dirs, missing_dirs, warnings

set -euo pipefail

SKILL_DIR="${1:?Usage: compare-structure.sh <skill-path>}"

if [[ ! -d "$SKILL_DIR" ]]; then
    echo '{"error":"'$SKILL_DIR' is not a directory"}'
    exit 1
fi

MISSING=()
WARNINGS=()
FOUND_DIRS=()
MISSING_DIRS=()

# Check for SKILL.md (required)
if [[ -f "$SKILL_DIR/SKILL.md" ]] || [[ -f "$SKILL_DIR/skill.md" ]]; then
    FOUND_DIRS+=("SKILL.md")
else
    MISSING+=("SKILL.md (required)")
fi

# Check for recommended directories
for d in scripts references assets; do
    if [[ -d "$SKILL_DIR/$d" ]]; then
        FOUND_DIRS+=("$d/")
    else
        MISSING_DIRS+=("$d/")
    fi
done

# Check for evals directory (best practice for testable skills)
if [[ -d "$SKILL_DIR/evals" ]]; then
    FOUND_DIRS+=("evals/")
    if [[ -f "$SKILL_DIR/evals/evals.json" ]]; then
        FOUND_DIRS+=("evals/evals.json")
    else
        WARNINGS+=("evals/ directory exists but no evals.json found")
    fi
else
    WARNINGS+=("No evals/ directory found. Consider adding evals/evals.json for test cases.")
fi

# Check scripts are executable if present
if [[ -d "$SKILL_DIR/scripts" ]]; then
    for f in "$SKILL_DIR/scripts/"*.sh; do
        [[ -f "$f" ]] || continue
        if [[ ! -x "$f" ]]; then
            WARNINGS+=("$(basename "$f") is not executable")
        fi
    done
fi

# Check SKILL.md line count (spec recommends <500)
SKILL_MD=$(find "$SKILL_DIR" -maxdepth 1 -iname "skill.md" | head -1)
if [[ -n "$SKILL_MD" ]]; then
    LINE_COUNT=$(wc -l < "$SKILL_MD")
    if (( LINE_COUNT > 500 )); then
        WARNINGS+=("SKILL.md has $LINE_COUNT lines. Spec recommends under 500.")
    fi
fi

# Calculate score: +1 per found optional dir, -1 per warning
SCORE=$(( ${#FOUND_DIRS[@]} - ${#MISSING[@]} * 2 ))
(( SCORE < 0 )) && SCORE=0
(( SCORE > 10 )) && SCORE=10

# Output JSON
FOUND_JSON=$(printf '%s\n' "${FOUND_DIRS[@]}" | jq -R . | jq -s . 2>/dev/null || echo '[]')
MISSING_JSON=$(printf '%s\n' "${MISSING_DIRS[@]}" | jq -R . | jq -s . 2>/dev/null || echo '[]')
WARN_JSON=$(printf '%s\n' "${WARNINGS[@]}" | jq -R . | jq -s . 2>/dev/null || echo '[]')

# Handle empty arrays gracefully
[[ ${#FOUND_DIRS[@]} -eq 0 ]] && FOUND_JSON='[]'
[[ ${#MISSING_DIRS[@]} -eq 0 ]] && MISSING_JSON='[]'
[[ ${#WARNINGS[@]} -eq 0 ]] && WARN_JSON='[]'

cat <<EOF
{
  "structure_score": $SCORE,
  "found": $FOUND_JSON,
  "missing_recommended": $MISSING_JSON,
  "warnings": $WARN_JSON
}
EOF
