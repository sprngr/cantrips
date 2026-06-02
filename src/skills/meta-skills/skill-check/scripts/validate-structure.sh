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

python3 - "$SKILL_MD" "$SKILL_DIR" <<'PY'
import json
import re
import sys
from pathlib import Path

import yaml


skill_md = Path(sys.argv[1])
skill_dir = Path(sys.argv[2])

results: list[dict[str, object]] = []


def add(check: str, passed: bool, detail: str) -> None:
    results.append({"check": check, "pass": passed, "detail": detail})


WINDOWS_PATH_RE = re.compile(
    r"(?:(?:[A-Za-z]:\\(?:[^\\\s]+\\)*[^\\\s]*)|(?:\b(?:\.{1,2}|[A-Za-z0-9_.-]+)(?:\\[A-Za-z0-9_. -]+)+))"
)


def find_windows_style_path(text: str) -> str | None:
    m = WINDOWS_PATH_RE.search(text)
    if not m:
        return None
    return m.group(0)


def strip_quoted_segments(text: str) -> str:
    return re.sub(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|`[^`]*`', '', text)


text = skill_md.read_text(encoding="utf-8")
add("SKILL.md_exists", True, f"Found {skill_md.name} at {skill_dir}")

starts = text.startswith("---")
add("frontmatter_starts", starts, "Frontmatter header present" if starts else "SKILL.md must start with ---")

frontmatter_text = ""
body_text = text
closes = False

if starts:
    lines = text.splitlines()
    closing_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            closing_idx = idx
            break

    closes = closing_idx is not None
    add(
        "frontmatter_closes",
        closes,
        "Frontmatter closing --- found" if closes else "Frontmatter not properly closed with ---",
    )

    if closes and closing_idx is not None:
        frontmatter_text = "\n".join(lines[1:closing_idx])
        body_text = "\n".join(lines[closing_idx + 1 :])
else:
    add("frontmatter_closes", False, "Frontmatter not properly closed with ---")

frontmatter_data = None
if closes:
    try:
        frontmatter_data = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter_data, dict):
            add("frontmatter_parse", False, "Frontmatter YAML must parse to a mapping object")
            frontmatter_data = None
        else:
            add("frontmatter_parse", True, "Frontmatter YAML parsed successfully")
    except Exception as exc:  # pragma: no cover
        add("frontmatter_parse", False, f"Frontmatter YAML parse error: {exc}")
else:
    add("frontmatter_parse", False, "Cannot parse frontmatter because delimiters are invalid")

if isinstance(frontmatter_data, dict):
    # name checks
    name = frontmatter_data.get("name")
    if isinstance(name, str) and name.strip():
        name_val = name.strip()
        add("name_present", True, f"name = {name_val}")
        add("name_lowercase", not any(ch.isupper() for ch in name_val), "name is lowercase" if not any(ch.isupper() for ch in name_val) else "name contains uppercase characters")
        add(
            "name_no_edge_hyphen",
            not (name_val.startswith("-") or name_val.endswith("-")),
            "name has no leading/trailing hyphen" if not (name_val.startswith("-") or name_val.endswith("-")) else "name starts or ends with hyphen",
        )
        add(
            "name_no_double_hyphen",
            "--" not in name_val,
            "name has no consecutive hyphens" if "--" not in name_val else "name contains consecutive hyphens",
        )
        add(
            "name_valid_chars",
            re.fullmatch(r"[a-z0-9-]+", name_val) is not None,
            "name contains only valid characters" if re.fullmatch(r"[a-z0-9-]+", name_val) is not None else "name contains invalid characters",
        )
        add(
            "name_length",
            len(name_val) <= 64,
            f"name within 64 char limit ({len(name_val)})" if len(name_val) <= 64 else f"name exceeds 64 chars ({len(name_val)})",
        )
        add(
            "name_matches_dir",
            name_val == skill_dir.name,
            "name matches directory name" if name_val == skill_dir.name else f"name '{name_val}' does not match directory '{skill_dir.name}'",
        )
    else:
        add("name_present", False, "Missing required field: name")

    # description checks
    description = frontmatter_data.get("description")
    if isinstance(description, str) and description.strip():
        desc = " ".join(description.split())
        add(
            "description_valid",
            len(desc) <= 1024,
            "description within 1024 char limit" if len(desc) <= 1024 else f"description exceeds 1024 chars ({len(desc)})",
        )
        has_use_when = re.search(r"\buse when\b", desc, flags=re.IGNORECASE) is not None
        add(
            "description_use_when",
            has_use_when,
            "description includes 'Use when' trigger phrase" if has_use_when else "description must include 'Use when' trigger phrase",
        )
        desc_without_quoted_examples = strip_quoted_segments(desc)
        third_person_ok = re.search(
            r"\b(i|me|my|mine|we|our|ours|you|your|yours)\b",
            desc_without_quoted_examples,
            flags=re.IGNORECASE,
        ) is None
        add(
            "description_third_person",
            third_person_ok,
            "description uses third-person wording" if third_person_ok else "description must avoid first/second-person pronouns",
        )
    else:
        add("description_valid", False, "Missing required field: description")
        add("description_use_when", False, "description must include 'Use when' trigger phrase")
        add("description_third_person", False, "description must avoid first/second-person pronouns")

    # allowed fields
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    unknown = sorted(set(frontmatter_data.keys()) - allowed)
    add(
        "no_unknown_fields",
        not unknown,
        "No unknown frontmatter fields" if not unknown else f"Unknown frontmatter fields: {', '.join(unknown)}",
    )

    # optional compatibility length
    compatibility = frontmatter_data.get("compatibility")
    if compatibility is None:
        add("compatibility_length", True, "compatibility field not present")
    elif isinstance(compatibility, str):
        add(
            "compatibility_length",
            len(compatibility) <= 500,
            "compatibility within 500 char limit" if len(compatibility) <= 500 else f"compatibility exceeds 500 chars ({len(compatibility)})",
        )
    else:
        add("compatibility_length", False, "compatibility must be a string when provided")
else:
    add("name_present", False, "Missing required field: name")
    add("description_valid", False, "Missing required field: description")
    add("description_use_when", False, "description must include 'Use when' trigger phrase")
    add("description_third_person", False, "description must avoid first/second-person pronouns")
    add("no_unknown_fields", False, "Cannot validate unknown fields: frontmatter parse failed")
    add("compatibility_length", False, "Cannot validate compatibility length: frontmatter parse failed")

windows_match = find_windows_style_path(body_text)
add(
    "no_windows_paths",
    windows_match is None,
    "No Windows-style paths found in SKILL.md body" if windows_match is None else f"Windows-style path detected: {windows_match}",
)

print(json.dumps(results, indent=2))
PY
