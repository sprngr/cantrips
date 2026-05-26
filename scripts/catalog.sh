#!/usr/bin/env bash
# Rebuild inventory/catalog.json from repo state
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
INVENTORY_DIR="$REPO_DIR/inventory"
CATALOG="$INVENTORY_DIR/catalog.json"

# shellcheck disable=SC1091
SCRIPT_ENV="$SCRIPT_DIR/.env"
if [ -f "$SCRIPT_ENV" ]; then
  . "$SCRIPT_ENV"
fi

# Generate timestamp
GENERATED=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Get git SHA for current repo
GIT_SHA=$(git -C "$REPO_DIR" rev-parse HEAD 2>/dev/null || echo "")

# Get source URL
if git -C "$REPO_DIR" remote get-url origin >/dev/null 2>&1; then
  SOURCE_URL=$(git -C "$REPO_DIR" remote get-url origin)
else
  SOURCE_URL="file://$REPO_DIR"
fi

# Get cantrips version from package.json if exists, else 0.0.0
if [ -f "$REPO_DIR/package.json" ]; then
  SOURCE_VERSION=$(grep -o '"version": *"[^"]*"' "$REPO_DIR/package.json" | head -1 | grep -o '[0-9]*\.[0-9]*\.[0-9]*' || echo "0.0.0")
else
  SOURCE_VERSION="0.0.0"
fi

# Start catalog
echo '{' > "$CATALOG"
echo "  \"generated\": \"$GENERATED\"," >> "$CATALOG"
echo '  "sources": [' >> "$CATALOG"
echo "    {\"name\": \"cantrips\", \"url\": \"$SOURCE_URL\", \"type\": \"local\", \"version\": \"$SOURCE_VERSION\"}" >> "$CATALOG"
echo '  ],' >> "$CATALOG"

# Skills
echo '  "skills": [' >> "$CATALOG"
FIRST_SKILL=true
for skill_dir in "$REPO_DIR"/skills/*/; do
  [ -d "$skill_dir" ] || continue
  skill_name=$(basename "$skill_dir")
  skill_path="skills/$skill_name"

  # Check for SKILL.md
  SKILL_FILE="$skill_dir/SKILL.md"
  if [ ! -f "$SKILL_FILE" ]; then
    continue
  fi

  # Extract version from frontmatter if exists
  version=$(grep -m1 '^version:' "$SKILL_FILE" 2>/dev/null | sed 's/^version: *//' || echo "")
  [ -z "$version" ] && version="null" && has_version="false" || has_version="true"
  [ "$has_version" = "true" ] && version="\"$version\""

  # Determine complexity
  complexity="playbook"

  # Check for scripts/references
  has_scripts=false
  has_references=false
  if ls "$skill_dir"/*.sh >/dev/null 2>&1; then
    has_scripts=true
  fi

  source="cantrips"
  if [ "$has_version" = "true" ] && [ -n "$version" ] && [ "${version//\"/}" != "" ]; then
    version="\"$version\""
  else
    version="null"
  fi

  # Determine if from upstream (was in archive) or cantrips original
  src="cantrips"
  if [ -d "$REPO_DIR/archive" ]; then
    if ls "$REPO_DIR/archive"/"$skill_name"*/ 2>/dev/null | head -1 >/dev/null 2>&1; then
      src="upstream"
    fi
  fi

  entry=$(cat <<ENTRY_EOF
    {
      "name": "$skill_name",
      "path": "$skill_path",
      "source": "$src",
      "version": $version,
      "complexity": "$complexity",
      "has_scripts": $has_scripts,
      "has_references": $has_references
    }
ENTRY_EOF
)

  if [ "$FIRST_SKILL" = true ]; then
    echo "$entry" >> "$CATALOG"
    FIRST_SKILL=false
  else
    echo "    ," >> "$CATALOG"
    echo "$entry" >> "$CATALOG"
  fi

  # Check archive for this skill's git info (skip for now, not tracked)
done
echo '  ],' >> "$CATALOG"

# Agents
echo '  "agents": [' >> "$CATALOG"
FIRST_AGENT=true
for agent_file in "$REPO_DIR"/agents/*.agent.md; do
  [ -f "$agent_file" ] || continue
  agent_name=$(basename "$agent_file" .agent.md)
  agent_path="agents/${agent_name}.agent.md"

  # Get git SHA for this specific file
  file_sha=$(git -C "$REPO_DIR" log -1 --format='%h' -- "$agent_file" 2>/dev/null || echo "HEAD")

  entry="    {\"name\": \"$agent_name\", \"path\": \"$agent_path\", \"source\": \"cantrips\", \"git_sha\": \"$file_sha\"}"

  if [ "$FIRST_AGENT" = true ]; then
    echo "$entry" >> "$CATALOG"
    FIRST_AGENT=false
  else
    echo "    ," >> "$CATALOG"
    echo "$entry" >> "$CATALOG"
  fi
done
echo '  ]' >> "$CATALOG"
echo '}' >> "$CATALOG"

echo "Catalog rebuilt: $CATALOG"