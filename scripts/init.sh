#!/usr/bin/env bash
# One-shot machine setup
# Clones/fetches cantrips repo → rebuilds catalog → syncs skills
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_ENV="$SCRIPT_DIR/.env"
HAS_ENV=false
if [ -f "$SCRIPT_ENV" ]; then
  . "$SCRIPT_ENV"
  HAS_ENV=true
fi

CLONE_DIR="${1:-$HOME/.agents}"
CLONE_URL="https://github.com/sprngr/cantrips.git"

echo "=== Cantrips Init ==="
echo ""

# 1. Clone cantrips
if [ -d "$CLONE_DIR/cantrips" ]; then
  echo "[1/3] Pulling latest cantrips..."
  git -C "$CLONE_DIR/cantrips" pull
else
  mkdir -p "$CLONE_DIR"
  echo "[1/3] Cloning cantrips $CLONE_URL → $CLONE_DIR/cantrips..."
  git clone "$CLONE_URL" "$CLONE_DIR/cantrips"
fi

# 2. Sync installed skills
CANTRIPS_SCRIPTS="$CLONE_DIR/cantrips/scripts"
if [ -f "$CANTRIPS_SCRIPTS/skills.sh" ]; then
  echo "[2/3] Running cantrips skills sync..."
  bash "$CANTRIPS_SCRIPTS/skills.sh sync"
else
  echo "[2/3] Skipping skills sync (skills.sh not found)"
fi

# 3. Rebuild catalog
if [ -f "$CANTRIPS_SCRIPTS/catalog.sh" ]; then
  echo "[3/3] Rebuilding catalog..."
  bash "$CANTRIPS_SCRIPTS/catalog.sh"
else
  echo "[3/3] Skipping catalog build (catalog.sh not found)"
fi

echo ""
echo "=== Done ==="