#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SRC="$ROOT/src/skills"
OUT="$ROOT/skills"

if [ ! -d "$SRC" ]; then
  echo "Missing source directory: $SRC" >&2
  exit 1
fi

rm -rf "$OUT"
mkdir -p "$OUT"

# Preserve category README files outside concrete skill directories.
if [ -f "$SRC/README.md" ]; then
  cp "$SRC/README.md" "$OUT/README.md"
fi

for category_readme in "$SRC"/*/README.md; do
  [ -f "$category_readme" ] || continue
  category_rel="${category_readme#"$SRC/"}"
  mkdir -p "$OUT/$(dirname "$category_rel")"
  cp "$category_readme" "$OUT/$category_rel"
done

while IFS= read -r -d '' skill_md; do
  skill_dir="$(dirname "$skill_md")"
  skill_rel="${skill_dir#"$SRC/"}"
  manifest="$skill_dir/.release-files"

  case "$skill_rel" in
    experimental/*)
      # Experimental skills remain source-only and are not promoted.
      continue
      ;;
  esac

  if [ ! -f "$manifest" ]; then
    echo "Missing manifest: $manifest" >&2
    exit 1
  fi

  mkdir -p "$OUT/$skill_rel"

  rsync -a --delete --prune-empty-dirs \
    --files-from="$manifest" \
    "$skill_dir/" "$OUT/$skill_rel/"

  # Strip development/test artifacts from promoted output.
  find "$OUT/$skill_rel" -type d \( -name tests -o -name __tests__ -o -name __pycache__ \) -prune -exec rm -rf {} +
  find "$OUT/$skill_rel" -type f \( \
    -name '*.test.*' -o \
    -name '*.spec.*' -o \
    -name '*.pyc' -o \
    -name '.DS_Store' -o \
    -name '.skill-plan.yaml' -o \
    -name '.skill-plan.patched.yaml' \
  \) -delete
done < <(find "$SRC" -type f -name 'SKILL.md' -print0)

echo "Built skills from $SRC -> $OUT"
