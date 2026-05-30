#!/usr/bin/env python3
"""Strict audit for tracked .skill-plan.yaml files.

Usage examples:
  python3 scripts/audit-skill-plans.py
  python3 scripts/audit-skill-plans.py --format json
  python3 scripts/audit-skill-plans.py --fail-on-violation
  python3 scripts/audit-skill-plans.py --files skills/experimental/squash/.skill-plan.yaml

Contract enforced from ADR-0002 (write-strict profile):
  - target_path is string, starts with skills/, ends with /, no leading /, no .. segments
  - enum fields are canonical values
  - workflow_notes is list[str]
  - coverage.essential_schema contains required boolean keys
  - coverage.unanswered_branches is array

Optional advisory warning:
  - experimental skills should live under skills/experimental/<skill>/
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML not installed. Install pyyaml to run audit.", file=sys.stderr)
    sys.exit(2)


ENUMS = {
    "scope": {"single", "moderate", "extended"},
    "mechanism": {"reasoning", "scripts", "hybrid"},
    "context_assets": {"none", "schema", "templates", "checklists", "manuals"},
    "tier": {"A", "B", "C"},
    "example_placed": {"inline", "references/Example.md"},
}

ESSENTIAL_COVERAGE_KEYS = [
    "intent",
    "scope",
    "mechanism",
    "context_assets",
    "tier",
    "target_path",
    "workflow_notes",
    "example_placed",
    "example_generated",
]


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return Path(result.stdout.strip())
    return Path.cwd()


def discovered_plan_files(root: Path) -> list[Path]:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return []
    return sorted(skills_root.rglob(".skill-plan.yaml"))


def violation(code: str, detail: str) -> dict[str, str]:
    return {"code": code, "detail": detail}


def audit_plan(path: Path, root: Path) -> dict[str, Any]:
    if path.is_absolute():
        try:
            rel = str(path.relative_to(root))
        except ValueError:
            rel = str(path)
    else:
        rel = str(path)
    output: dict[str, Any] = {"file": rel, "status": "ok", "violations": [], "warnings": []}

    try:
        raw = path.read_text(encoding="utf-8")
        data = yaml.safe_load(raw)
    except Exception as exc:
        output["status"] = "parse_error"
        output["violations"].append(violation("parse_error", str(exc)))
        return output

    if not isinstance(data, dict):
        output["status"] = "violation"
        output["violations"].append(violation("top_level_not_mapping", "Top-level YAML must be mapping"))
        return output

    # target_path rules
    target_path = data.get("target_path")
    if not isinstance(target_path, str) or not target_path.strip():
        output["violations"].append(violation("target_path_not_string", "target_path must be non-empty string"))
    else:
        if target_path.startswith("/"):
            output["violations"].append(violation("target_path_abs", "target_path must be relative, not absolute"))
        if not target_path.startswith("skills/"):
            output["violations"].append(
                violation("target_path_not_skills_prefix", "target_path must start with skills/")
            )
        if not target_path.endswith("/"):
            output["violations"].append(
                violation("target_path_no_trailing_slash", "target_path must end with /")
            )
        if ".." in target_path.split("/"):
            output["violations"].append(
                violation("target_path_parent_traversal", "target_path must not contain '..' segments")
            )

    # experimental convention warning (advisory, non-failing)
    skill_dir_name = Path(rel).parent.name
    if skill_dir_name in {"goblin-mode", "squash"} and "skills/experimental/" not in rel:
        if isinstance(target_path, str) and not target_path.startswith("skills/experimental/"):
            output["warnings"].append(
                violation(
                    "experimental_path_convention",
                    "experimental skill should target skills/experimental/<skill>/",
                )
            )

    # enum rules
    for key, allowed_values in ENUMS.items():
        value = data.get(key)
        if not isinstance(value, str) or value not in allowed_values:
            output["violations"].append(
                violation(
                    f"enum_{key}",
                    f"{key} must be one of {sorted(allowed_values)}",
                )
            )

    # workflow_notes rule
    notes = data.get("workflow_notes")
    if not (isinstance(notes, list) and all(isinstance(item, str) for item in notes)):
        output["violations"].append(
            violation("workflow_notes_not_list_of_strings", "workflow_notes must be list of strings")
        )

    # coverage rule
    coverage = data.get("coverage")
    if not isinstance(coverage, dict):
        output["violations"].append(violation("coverage_missing", "coverage block missing or not object"))
    else:
        essential = coverage.get("essential_schema")
        if not isinstance(essential, dict):
            output["violations"].append(
                violation("coverage_missing_essential_schema", "coverage.essential_schema missing or not object")
            )
        else:
            missing_keys = [k for k in ESSENTIAL_COVERAGE_KEYS if k not in essential]
            if missing_keys:
                output["violations"].append(
                    violation("coverage_missing_keys", f"coverage.essential_schema missing keys: {missing_keys}")
                )
            non_boolean_keys = [k for k in ESSENTIAL_COVERAGE_KEYS if k in essential and not isinstance(essential[k], bool)]
            if non_boolean_keys:
                output["violations"].append(
                    violation("coverage_non_boolean", f"coverage.essential_schema non-boolean keys: {non_boolean_keys}")
                )

        unanswered = coverage.get("unanswered_branches")
        if not isinstance(unanswered, list):
            output["violations"].append(
                violation("coverage_unanswered_not_array", "coverage.unanswered_branches must be array")
            )

    if output["violations"]:
        output["status"] = "violation"

    return output


def render_human(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    summary = payload["summary"]
    counts = payload["violation_counts"]
    warning_counts = payload["warning_counts"]

    lines.append("Skill-plan strict audit")
    lines.append(f"Files audited: {summary['total_files']}")
    lines.append(f"Files with violations: {summary['files_with_violations']}")
    lines.append(f"Total violations: {summary['total_violations']}")
    lines.append(f"Total warnings: {summary['total_warnings']}")
    lines.append("")

    if counts:
        lines.append("Violation counts:")
        for code, n in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"  - {code}: {n}")
        lines.append("")

    if warning_counts:
        lines.append("Warning counts (advisory):")
        for code, n in sorted(warning_counts.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"  - {code}: {n}")
        lines.append("")

    lines.append("Per-file results:")
    for item in payload["files"]:
        lines.append(f"- {item['file']} [{item['status']}]")
        for v in item["violations"]:
            lines.append(f"    * {v['code']}: {v['detail']}")
        for w in item.get("warnings", []):
            lines.append(f"    ! {w['code']}: {w['detail']}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Strict audit for tracked .skill-plan.yaml files")
    parser.add_argument(
        "--format",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human)",
    )
    parser.add_argument(
        "--fail-on-violation",
        action="store_true",
        help="Exit with code 1 when any violation exists",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        default=None,
        help="Optional explicit .skill-plan.yaml files to audit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()

    if args.files:
        files = [Path(f).resolve() if not Path(f).is_absolute() else Path(f) for f in args.files]
    else:
        files = discovered_plan_files(root)

    results = [audit_plan(path, root) for path in files]

    counter: Counter[str] = Counter()
    warning_counter: Counter[str] = Counter()
    files_with_violations = 0
    total_violations = 0
    total_warnings = 0

    for item in results:
        if item["violations"]:
            files_with_violations += 1
            total_violations += len(item["violations"])
        for v in item["violations"]:
            counter[v["code"]] += 1
        total_warnings += len(item.get("warnings", []))
        for w in item.get("warnings", []):
            warning_counter[w["code"]] += 1

    payload = {
        "summary": {
            "total_files": len(results),
            "files_with_violations": files_with_violations,
            "total_violations": total_violations,
            "total_warnings": total_warnings,
        },
        "violation_counts": dict(counter),
        "warning_counts": dict(warning_counter),
        "files": results,
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(render_human(payload))

    if args.fail_on_violation and total_violations > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
