#!/usr/bin/env bash
# diff-snapshot.sh - Compare before/after skill directory snapshots
# Usage: scripts/diff-snapshot.sh <before-dir> <after-dir>
# Output: File-level diff summary (added, removed, modified files + line counts)

set -euo pipefail
LC_ALL=C

BEFORE="${1:?Usage: diff-snapshot.sh <before-dir> <after-dir>}"
AFTER="${2:?Usage: diff-snapshot.sh <before-dir> <after-dir>}"

if [[ ! -d "$BEFORE" ]]; then
    echo "Error: before directory not found: $BEFORE" >&2
    exit 1
fi

if [[ ! -d "$AFTER" ]]; then
    echo "Error: after directory not found: $AFTER" >&2
    exit 1
fi

echo "=== Diff Summary ==="
echo "Before: $BEFORE"
echo "After:  $AFTER"
echo ""

declare -A BEFORE_SET=()
declare -A AFTER_SET=()

declare -a ADDED_FILES=()
declare -a REMOVED_FILES=()
declare -a MODIFIED_FILES=()

sort_array() {
    local -n source_arr="$1"
    local -n sorted_arr="$2"

    if (( ${#source_arr[@]} == 0 )); then
        sorted_arr=()
        return
    fi

    mapfile -d '' sorted_arr < <(printf '%s\0' "${source_arr[@]}" | sort -z)
}

# Find all files in both directories (relative paths), null-delimited for safety.
while IFS= read -r -d '' f; do
    BEFORE_SET["$f"]=1
done < <(cd "$BEFORE" && find . -type f -print0)

while IFS= read -r -d '' f; do
    AFTER_SET["$f"]=1
done < <(cd "$AFTER" && find . -type f -print0)

# Added files (in after but not before)
for f in "${!AFTER_SET[@]}"; do
    [[ -n "${BEFORE_SET[$f]+x}" ]] && continue
    ADDED_FILES+=("$f")
done

# Removed files (in before but not after)
for f in "${!BEFORE_SET[@]}"; do
    [[ -n "${AFTER_SET[$f]+x}" ]] && continue
    REMOVED_FILES+=("$f")
done

# Modified files (in both, content differs)
for f in "${!BEFORE_SET[@]}"; do
    [[ -n "${AFTER_SET[$f]+x}" ]] || continue
    if ! diff -q "$BEFORE/$f" "$AFTER/$f" > /dev/null 2>&1; then
        MODIFIED_FILES+=("$f")
    fi
done

sort_array ADDED_FILES ADDED_SORTED
sort_array REMOVED_FILES REMOVED_SORTED
sort_array MODIFIED_FILES MODIFIED_SORTED

if (( ${#ADDED_SORTED[@]} > 0 )); then
    echo "--- Added ---"
    for f in "${ADDED_SORTED[@]}"; do
        LINES=$(wc -l < "$AFTER/$f" 2>/dev/null || echo "0")
        printf '  + %q (%s lines)\n' "$f" "$LINES"
    done
    echo ""
fi

if (( ${#REMOVED_SORTED[@]} > 0 )); then
    echo "--- Removed ---"
    for f in "${REMOVED_SORTED[@]}"; do
        LINES=$(wc -l < "$BEFORE/$f" 2>/dev/null || echo "0")
        printf '  - %q (%s lines)\n' "$f" "$LINES"
    done
    echo ""
fi

if (( ${#MODIFIED_SORTED[@]} > 0 )); then
    echo "--- Modified ---"
    MODIFIED=false
    for f in "${MODIFIED_SORTED[@]}"; do
        DIFF_STATS=$(diff --unified=0 "$BEFORE/$f" "$AFTER/$f" 2>/dev/null | grep -cE '^\+[^+]|^-[^-]' || echo "0")
        printf '  ~ %q (%s changed lines)\n' "$f" "$DIFF_STATS"
        MODIFIED=true
    done
    echo ""
fi

# Summary counts
ADDED_COUNT=${#ADDED_SORTED[@]}
REMOVED_COUNT=${#REMOVED_SORTED[@]}
MOD_COUNT=${#MODIFIED_SORTED[@]}

echo "=== Totals ==="
echo "  Added:    $ADDED_COUNT"
echo "  Removed:  $REMOVED_COUNT"
echo "  Modified: $MOD_COUNT"
