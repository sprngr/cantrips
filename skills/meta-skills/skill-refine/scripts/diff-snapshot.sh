#!/usr/bin/env bash
# diff-snapshot.sh - Compare before/after skill directory snapshots
# Usage: scripts/diff-snapshot.sh <before-dir> <after-dir>
# Output: File-level diff summary (added, removed, modified files + line counts)

set -euo pipefail

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

# Find all files in both directories (relative paths)
BEFORE_FILES=$(cd "$BEFORE" && find . -type f | sort)
AFTER_FILES=$(cd "$AFTER" && find . -type f | sort)

# Added files (in after but not before)
ADDED=$(comm -13 <(echo "$BEFORE_FILES") <(echo "$AFTER_FILES"))
if [[ -n "$ADDED" ]]; then
    echo "--- Added ---"
    while IFS= read -r f; do
        LINES=$(wc -l < "$AFTER/$f" 2>/dev/null || echo "0")
        echo "  + $f ($LINES lines)"
    done <<< "$ADDED"
    echo ""
fi

# Removed files (in before but not after)
REMOVED=$(comm -23 <(echo "$BEFORE_FILES") <(echo "$AFTER_FILES"))
if [[ -n "$REMOVED" ]]; then
    echo "--- Removed ---"
    while IFS= read -r f; do
        LINES=$(wc -l < "$BEFORE/$f" 2>/dev/null || echo "0")
        echo "  - $f ($LINES lines)"
    done <<< "$REMOVED"
    echo ""
fi

# Modified files (in both, content differs)
COMMON=$(comm -12 <(echo "$BEFORE_FILES") <(echo "$AFTER_FILES"))
if [[ -n "$COMMON" ]]; then
    MODIFIED=false
    while IFS= read -r f; do
        if ! diff -q "$BEFORE/$f" "$AFTER/$f" > /dev/null 2>&1; then
            if [[ "$MODIFIED" == false ]]; then
                echo "--- Modified ---"
                MODIFIED=true
            fi
            DIFF_STATS=$(diff --unified=0 "$BEFORE/$f" "$AFTER/$f" 2>/dev/null | grep -cE '^\+[^+]|^-[^-]' || echo "0")
            echo "  ~ $f ($DIFF_STATS changed lines)"
        fi
    done <<< "$COMMON"
    if [[ "$MODIFIED" == true ]]; then
        echo ""
    fi
fi

# Summary counts
ADDED_COUNT=$(echo "$ADDED" | grep -c . 2>/dev/null || echo "0")
REMOVED_COUNT=$(echo "$REMOVED" | grep -c . 2>/dev/null || echo "0")
MOD_COUNT=0
if [[ -n "$COMMON" ]]; then
    while IFS= read -r f; do
        if ! diff -q "$BEFORE/$f" "$AFTER/$f" > /dev/null 2>&1; then
            MOD_COUNT=$((MOD_COUNT + 1))
        fi
    done <<< "$COMMON"
fi

echo "=== Totals ==="
echo "  Added:    $ADDED_COUNT"
echo "  Removed:  $REMOVED_COUNT"
echo "  Modified: $MOD_COUNT"
