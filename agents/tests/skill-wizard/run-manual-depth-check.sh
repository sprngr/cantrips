#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

CHECKLIST_PATH="$REPO_ROOT/agents/tests/skill-wizard/depth-checklist.md"
RUNSHEET_PATH="$REPO_ROOT/agents/tests/skill-wizard/depth-runsheet.md"
FIXTURE_PATH="$REPO_ROOT/agents/tests/skill-wizard/fixtures/resume-incomplete.skill-plan.yaml"

cat <<EOF
Skill-wizard manual depth-check helper

Checklist:
  $CHECKLIST_PATH

Runsheet:
  $RUNSHEET_PATH

SW-D06 fixture copy command:
  cp "$FIXTURE_PATH" ./.skill-plan.yaml
EOF
