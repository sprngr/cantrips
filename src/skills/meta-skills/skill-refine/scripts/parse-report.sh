#!/usr/bin/env bash
# parse-report.sh - Extract JSON summary from skill-check or skill-eval HTML reports
# Usage: scripts/parse-report.sh <report-html-path>
# Output: JSON object to stdout (the {{JSON_SUMMARY}} block from the report)

set -euo pipefail

REPORT="${1:?Usage: parse-report.sh <report-html-path>}"

if [[ ! -f "$REPORT" ]]; then
    echo '{"error":"Report file not found: '"$REPORT"'"}' >&2
    exit 1
fi

python3 "$(dirname "$0")/parse_report.py" "$REPORT"
