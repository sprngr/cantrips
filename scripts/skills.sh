#!/usr/bin/env bash
# Cantrips skills management wrapper around npx skills CLI
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
INVENTORY_DIR="$REPO_DIR/inventory"

# Load defaults
SCRIPT_ENV="$SCRIPT_DIR/.env"
if [ -f "$SCRIPT_ENV" ]; then
  . "$SCRIPT_ENV"
fi

# Registry location
REGISTRY_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/cantrips"
REGISTRY_FILE="$REGISTRY_DIR/registry.json"

# Ensure registry directory exists
ensure_registry() {
  mkdir -p "$REGISTRY_DIR"
  if [ ! -f "$REGISTRY_FILE" ]; then
    echo '{}' | python3 -m json.tool > "$REGISTRY_FILE" 2>/dev/null || echo '{}' > "$REGISTRY_FILE"
  fi
}

# Get registry value
get_reg() {
  local key="$1"
  python3 -c "
import json, sys
with open('$REGISTRY_FILE') as f:
    d = json.load(f)
keys = '$key'.split('.')
v = d
for k in keys:
    v = v[k]
if isinstance(v, dict) or isinstance(v, list):
    print(json.dumps(v))
else:
    print(v if v is not None else '')
" 2>/dev/null || echo ""
}

# Set registry value
set_reg() {
  local key="$1" val="$2"
  python3 -c "
import json
with open('$REGISTRY_FILE') as f:
    d = json.load(f)
keys = '$key'.split('.')
v = d
for k in keys[:-1]:
    if k not in v:
        v[k] = {}
    v = v[k]
try:
    v[keys[-1]] = json.loads('''$val''')
except (json.JSONDecodeError, ValueError):
    v[keys[-1]] = '''$val'''
with open('$REGISTRY_FILE', 'w') as f:
    json.dump(d, f, indent=2)
"
}

# Init registry - add cantrips as local source
cmd_init() {
  ensure_registry

  # Add cantrips as local source
  local name="cantrips"
  local existing=$(get_reg "sources.$name" || echo "")
  if [ -n "$existing" ]; then
    echo "Source '$name' already exists in registry."
    return 0
  fi

  # Store local source
  local url="file://$REPO_DIR"
  python3 -c "
import json
with open('$REGISTRY_FILE') as f:
    d = json.load(f)
d['sources']['cantrips'] = {'url': '$url', 'type': 'local', 'version': '0.0.0'}
with open('$REGISTRY_FILE', 'w') as f:
    json.dump(d, f, indent=2)
"

  echo "Initialized registry at $REGISTRY_FILE"
  echo "Local source 'cantrips' registered: $url"
}

# Add skill
cmd_add() {
  ensure_registry
  if [ $# -ge 2 ]; then
    local source="$1"
    local skill_name="$2"
    shift 2
  elif [ $# -eq 1 ]; then
    local skill_name="$1"
    local src_data
    src_data=$(get_reg "installed_skills.$skill_name.source" || echo "")
    if [ -z "$src_data" ]; then
      echo "Skill '$skill_name' not found in registry. To add a new skill, use: $0 add <source> <name>"
      return 1
    fi
    local source="$src_data"
  else
    echo "Usage: $0 add <source> <skill-name>"
    return 1
  fi
  local extra_args="$*"

  # Add to npx skills
  local npx_opts="npx $SKILLS_PKG add"
  [ -n "$INSTALL_TARGET" ] && npx_opts="$npx_opts $INSTALL_TARGET"
  [ -n "$NPX_ARGS" ] && npx_opts="$npx_opts $NPX_ARGS"

  echo "Adding skill: $source/$skill_name"
  eval "$npx_opts --skill $skill_name 2>/dev/null || npx $SKILLS_PKG add --skill $skill_name $extra_args"

  # Register in cantrips registry
  local reg_source
  if [[ "$source" == file://* ]] || [[ "$source" == / ]]; then
    reg_source="local"
  else
    reg_source="github"
  fi

  # Add to installed_skills
  python3 -c "
import json, datetime
with open('$REGISTRY_FILE') as f:
    d = json.load(f)
d['installed_skills']['$skill_name'] = {
    'source': '$source',
    'source_type': '$reg_source',
    'added_at': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'version': None
}
with open('$REGISTRY_FILE', 'w') as f:
    json.dump(d, f, indent=2)
"

  echo "Registered '$skill_name' in $REGISTRY_FILE"
}

# Update skill
cmd_update() {
  ensure_registry
  local skill="${1:-}"

  if [ -n "$skill" ]; then
    echo "Updating skill: $skill"
    npx $SKILLS_PKG update --skill "$skill" ${NPX_ARGS:-} 2>/dev/null || echo "Update failed for $skill (non-fatal)"

    # Update timestamp
    python3 -c "
import json, datetime
with open('$REGISTRY_FILE') as f:
    d = json.load(f)
if '$skill' in d.get('installed_skills', {}):
    d['installed_skills']['$skill']['updated_at'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    with open('$REGISTRY_FILE', 'w') as f:
        json.dump(d, f, indent=2)
"
    echo "Updated $skill"
  else
    echo "Updating all skills..."
    for skill in $(python3 -c "import json; d=json.load(open('$REGISTRY_FILE')); print(' '.join(d.get('installed_skills', {}).keys()))"); do
      cmd_update "$skill"
    done
    echo "All skills updated."
  fi
}

# Remove skill
cmd_remove() {
  ensure_registry
  [ $# -ge 1 ] || { echo "Usage: $0 remove <skill-name>"; return 1; }

  local skill="$1"
  echo "Removing skill: $skill"

  # Uninstall from npx skills if applicable
  npx $SKILLS_PKG rm --skill "$skill" 2>/dev/null || true

  # Remove from registry
  python3 -c "
import json
with open('$REGISTRY_FILE') as f:
    d = json.load(f)
d['installed_skills'].pop('$skill', None)
with open('$REGISTRY_FILE', 'w') as f:
    json.dump(d, f, indent=2)
"



  echo "Removed $skill"
}

# Sync all registered skills
cmd_sync() {
  ensure_registry
  echo "Syncing all registered skills..."

  local skills_keys
  skills_keys=$(python3 -c "import json; d=json.load(open('$REGISTRY_FILE')); print(' '.join(d.get('installed_skills', {}).keys()))")
  if [ -z "$skills_keys" ]; then
    echo "No skills registered."
    return 0
  fi

  for skill in $skills_keys; do
    local src
    src=$(get_reg "installed_skills.$skill.source" || echo "")
    if [ -n "$src" ]; then
      cmd_add "$src" "$skill"
    else
      echo "Skipping $skill (no source registered)"
    fi
  done

  echo "Sync complete."
}

# List registry contents
cmd_ls() {
  ensure_registry
  python3 -c "
import json
with open('$REGISTRY_FILE') as f:
    d = json.load(f)
sources = d.get('sources', {})
installed = d.get('installed_skills', {})
print(f'Registry: {REGISTRY_FILE}')
print(f'Sources: {len(sources)}')
for name, info in sources.items():
    print(f'  [{info.get(\"type\", \"?\")}] {name} @ {info.get(\"url\", \"?\")}')
print(f'Installed: {len(installed)}')
for name, info in installed.items():
    v = info.get('version') or 'n/a'
    src = info.get('source_type', '?')
    print(f'  [{src}] {name} (v{v})')
"
}

# Find skills
cmd_find() {
  [ $# -ge 1 ] || { echo "Usage: $0 find <query>"; return 1; }
  npx $SKILLS_PKG find "$@"
}

# Main command routing
CMD="${1:-help}"
shift 2>/dev/null || true

case "$CMD" in
  init)     cmd_init ;;
  add)      cmd_add "$@" ;;
  update)   cmd_update "$@" ;;
  remove)   cmd_remove "$@" ;;
  sync)     cmd_sync ;;
  ls)       cmd_ls ;;
  find)     cmd_find "$@" ;;
  help|--help|-h)
    echo "Usage: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  init              Initialize registry, add cantrips as local source"
    echo "  add <source> <skill>  Add skill to registry"
    echo "  update [skill]    Update specific skill or all"
    echo "  remove <skill>    Remove skill from registry"
    echo "  sync              Sync all registered skills"
    echo "  ls [flags]        List registry state"
    echo "  find <query>      Proxy to npx skills find"
    exit 0
    ;;
  *)
    echo "Unknown command: $CMD"
    echo "Run '$0 help' for usage."
    exit 1
    ;;
esac