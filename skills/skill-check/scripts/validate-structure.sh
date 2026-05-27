#!/usr/bin/env bash
# validate-structure.sh - Structural validation of SKILL.md frontmatter
# Usage: scripts/validate-structure.sh <skill-path>
# Output: JSON array of {check, pass, detail} objects

set -euo pipefail

SKILL_DIR="${1:?Usage: validate-structure.sh <skill-path>}"

if [[ ! -d "$SKILL_DIR" ]]; then
    echo "Error: $SKILL_DIR is not a directory" >&2
    exit 1
fi

SKILL_MD=""
[[ -f "$SKILL_DIR/SKILL.md" ]] && SKILL_MD="$SKILL_DIR/SKILL.md"
[[ -f "$SKILL_DIR/skill.md" ]] && SKILL_MD="$SKILL_DIR/skill.md"

if [[ -z "$SKILL_MD" ]]; then
    echo '[{"check":"SKILL.md_exists","pass":false,"detail":"Missing required file: SKILL.md"}]'
    exit 0
fi

RESULTS=()
add() { RESULTS+=("{\"check\":\"$1\",\"pass\":$2,\"detail\":\"$3\"}"); }

# 1. SKILL.md exists
add "SKILL.md_exists" true "Found $(basename "$SKILL_MD") at $SKILL_DIR"

# 2. Starts with frontmatter
FIRST_LINE=$(head -c3 "$SKILL_MD")
if [[ "$FIRST_LINE" != "---" ]]; then
    add "frontmatter_starts" false "SKILL.md must start with ---"
else
    add "frontmatter_starts" true "Frontmatter header present"
fi

# 3. Frontmatter closes
if grep -q '^---' "$SKILL_MD" | head -2 | tail -1 > /dev/null 2>&1; then
    add "frontmatter_closes" true "Frontmatter closing --- found"
else
    add "frontmatter_closes" false "Frontmatter not properly closed with ---"
fi

# 4. Extract YAML block (between first two ---)
YAML_BLOCK=$(awk '/^---/{n++;if(n==2){exit}}n==1{print}' "$SKILL_MD")

# 5. Check required field: name
if echo "$YAML_BLOCK" | grep -q '^name:'; then
    NAME_VAL=$(echo "$YAML_BLOCK" | grep '^name:' | sed 's/^name:[[:space:]]*//' | sed 's/^"//' | sed 's/"$//' | sed "s/'//g")
    add "name_present" true "name = $NAME_VAL"

    # name: lowercase only
    if echo "$NAME_VAL" | grep -q '[A-Z]'; then
        add "name_lowercase" false "name contains uppercase characters"
    else
        add "name_lowercase" true "name is lowercase"
    fi

    # name: no leading/trailing hyphen
    if [[ "$NAME_VAL" == -* ]] || [[ "$NAME_VAL" == *- ]]; then
        add "name_no_edge_hyphen" false "name starts or ends with hyphen"
    else
        add "name_no_edge_hyphen" true "name has no leading/trailing hyphen"
    fi

    # name: no consecutive hyphens
    if echo "$NAME_VAL" | grep -q '\-\-'; then
        add "name_no_double_hyphen" false "name contains consecutive hyphens"
    else
        add "name_no_double_hyphen" true "name has no consecutive hyphens"
    fi

    # name: valid chars only (lowercase alnum + hyphen)
    if echo "$NAME_VAL" | grep -qE '^[a-z0-9-]+$'; then
        add "name_valid_chars" true "name contains only valid characters"
    else
        add "name_valid_chars" false "name contains invalid characters"
    fi

    # name: length check
    NAME_LEN=${#NAME_VAL}
    if (( NAME_LEN > 64 )); then
        add "name_length" false "name exceeds 64 chars ($NAME_LEN)"
    else
        add "name_length" true "name within 64 char limit ($NAME_LEN)"
    fi

    # name: matches directory
    DIR_NAME=$(basename "$SKILL_DIR")
    if [[ "$NAME_VAL" == "$DIR_NAME" ]]; then
        add "name_matches_dir" true "name matches directory name"
    else
        add "name_matches_dir" false "name '$NAME_VAL' does not match directory '$DIR_NAME'"
    fi
else
    add "name_present" false "Missing required field: name"
fi

# 6. Check required field: description
if echo "$YAML_BLOCK" | grep -q '^description:'; then
    DESC_LEN=$(echo "$YAML_BLOCK" | grep '^description:' | sed 's/^description:[[:space:]]*//' | wc -c)
    if (( DESC_LEN > 1025 )); then
        add "description_valid" false "description exceeds 1024 chars"
    else
        add "description_valid" true "description within 1024 char limit"
    fi
else
    add "description_valid" false "Missing required field: description"
fi

# 7. Check for unknown fields
ALLOWED="name|description|license|compatibility|metadata|allowed-tools"
UNKNOWN=$(echo "$YAML_BLOCK" | grep -E '^[a-z]' | cut -d: -f1 | grep -vE "^($ALLOWED)$" || true)
if [[ -n "$UNKNOWN" ]]; then
    add "no_unknown_fields" false "Unknown frontmatter fields: $UNKNOWN"
else
    add "no_unknown_fields" true "No unknown frontmatter fields"
fi

# 8. Check optional field lengths if present
if echo "$YAML_BLOCK" | grep -q '^compatibility:'; then
    COMP_LEN=$(echo "$YAML_BLOCK" | grep '^compatibility:' | sed 's/^compatibility:[[:space:]]*//' | wc -c)
    if (( COMP_LEN > 501 )); then
        add "compatibility_length" false "compatibility exceeds 500 chars"
    else
        add "compatibility_length" true "compatibility within 500 char limit"
    fi
fi

# Output JSON array
echo "["
for i in "${!RESULTS[@]}"; do
    [[ $i -gt 0 ]] && echo ","
    printf "  %s" "${RESULTS[$i]}"
done
echo ""
echo "]"
