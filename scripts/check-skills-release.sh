#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SRC="$ROOT/src/skills"
OUT="$ROOT/skills"
OUT_REL="skills"

if [ ! -d "$SRC" ]; then
  echo "Missing source directory: $SRC" >&2
  exit 1
fi

fail=0

while IFS= read -r -d '' skill_md; do
  skill_dir="$(dirname "$skill_md")"
  skill_rel="${skill_dir#"$SRC/"}"
  manifest="$skill_dir/.release-files"

  case "$skill_rel" in
    experimental/*)
      # Experimental skills stay in src/skills only; still audited elsewhere.
      continue
      ;;
  esac

  if [ ! -f "$manifest" ]; then
    echo "Missing manifest for $skill_rel: $manifest" >&2
    fail=1
    continue
  fi

  if ! grep -qx 'SKILL.md' "$manifest"; then
    echo "Manifest missing SKILL.md entry: $manifest" >&2
    fail=1
  fi

  while IFS= read -r entry || [ -n "$entry" ]; do
    entry_trimmed="${entry#${entry%%[![:space:]]*}}"
    entry_trimmed="${entry_trimmed%${entry_trimmed##*[![:space:]]}}"

    if [ -z "$entry_trimmed" ]; then
      continue
    fi

    case "$entry_trimmed" in
      .skill-plan*|*tests/*|*/tests/*|*__tests__/*|*.test.*|*.spec.*)
        echo "Forbidden release entry in $manifest: $entry_trimmed" >&2
        fail=1
        continue
        ;;
    esac

    if [ ! -e "$skill_dir/$entry_trimmed" ]; then
      echo "Manifest path missing in $skill_rel: $entry_trimmed" >&2
      fail=1
    fi
  done < "$manifest"
done < <(find "$SRC" -type f -name 'SKILL.md' -print0)

if [ "$fail" -ne 0 ]; then
  exit 1
fi

before_status="$(git status --porcelain -- "$OUT_REL" || true)"

bash "$ROOT/scripts/build-skills.sh"

forbidden_paths=$(find "$OUT" \( \
  -type d \( -name tests -o -name __tests__ -o -name __pycache__ \) -o \
  -type f \( \
    -name '.release-files' -o \
    -name '.skill-plan.yaml' -o \
    -name '.skill-plan.patched.yaml' -o \
    -name '*.test.*' -o \
    -name '*.spec.*' -o \
    -name '*.pyc' -o \
    -name '.DS_Store' \
  \) \
\) -print)

if [ -n "$forbidden_paths" ]; then
  echo "Forbidden artifacts detected in promoted skills output:" >&2
  printf '%s\n' "$forbidden_paths" >&2
  exit 1
fi

experimental_promoted=$(find "$OUT/experimental" -mindepth 1 ! -path "$OUT/experimental/README.md" -print)
if [ -n "$experimental_promoted" ]; then
  echo "Only skills/experimental/README.md is allowed in promoted output." >&2
  printf '%s\n' "$experimental_promoted" >&2
  exit 1
fi

after_status="$(git status --porcelain -- "$OUT_REL" || true)"

if [ "$before_status" != "$after_status" ]; then
  echo "Promoted skills output is stale. Run: bash scripts/build-skills.sh" >&2
  git diff --name-only -- "$OUT_REL" >&2
  exit 1
fi

echo "Skills release checks passed."
