#!/usr/bin/env python3
"""Audit SKILL.md documentation contracts.

Hard-fail checks (violations):
  - frontmatter delimiters + YAML parse validity
  - required frontmatter fields (`name`, `description`) present and non-empty strings
  - no Windows-style paths in SKILL.md content

Warn-only checks:
  - SKILL.md body line count > 500
  - description appears to summarize workflow steps
  - description trigger keyword coverage appears sparse
  - nested markdown reference depth (>1 hop from SKILL.md)
"""

from __future__ import annotations

import argparse
import json
import re
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


WINDOWS_PATH_RE = re.compile(
    r"(?:(?:[A-Za-z]:\\(?:[^\\\s]+\\)*[^\\\s]*)|(?:\b(?:\.{1,2}|[A-Za-z0-9_.-]+)(?:\\[A-Za-z0-9_. -]+)+))"
)
WORKFLOW_SUMMARY_RE = re.compile(
    r"\b(first|then|next|step\s*\d|workflow|pipeline|phase|stage)\b",
    flags=re.IGNORECASE,
)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "when",
    "user",
    "use",
    "into",
    "your",
    "their",
    "before",
    "after",
    "then",
    "or",
    "and",
}


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


def safe_rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def discovered_skill_docs(root: Path) -> list[Path]:
    skills_root = root / "src" / "skills"
    if not skills_root.is_dir():
        skills_root = root / "skills"
    if not skills_root.is_dir():
        return []
    return sorted(skills_root.rglob("SKILL.md"))


def finding(code: str, detail: str) -> dict[str, str]:
    return {"code": code, "detail": detail}


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str, str, list[dict[str, str]]]:
    violations: list[dict[str, str]] = []
    if not text.startswith("---"):
        violations.append(finding("frontmatter_missing_start", "SKILL.md must start with ---"))
        return None, "", text, violations

    lines = text.splitlines()
    closing_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            closing_idx = idx
            break

    if closing_idx is None:
        violations.append(
            finding("frontmatter_missing_close", "Frontmatter not properly closed with ---")
        )
        return None, "", text, violations

    frontmatter_text = "\n".join(lines[1:closing_idx])
    body_text = "\n".join(lines[closing_idx + 1 :])

    try:
        data = yaml.safe_load(frontmatter_text)
    except Exception as exc:
        violations.append(finding("frontmatter_parse_error", f"Frontmatter YAML parse error: {exc}"))
        return None, frontmatter_text, body_text, violations

    if not isinstance(data, dict):
        violations.append(
            finding("frontmatter_not_mapping", "Frontmatter YAML must parse to mapping object")
        )
        return None, frontmatter_text, body_text, violations

    return data, frontmatter_text, body_text, violations


def find_windows_style_path(text: str) -> str | None:
    match = WINDOWS_PATH_RE.search(text)
    if not match:
        return None
    return match.group(0)


def extract_md_links(md_file: Path) -> list[str]:
    try:
        text = md_file.read_text(encoding="utf-8")
    except Exception:
        return []
    links: list[str] = []
    for m in LINK_RE.finditer(text):
        target = m.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if target.endswith(".md"):
            links.append(target)
    return links


def description_trigger_token_count(description: str) -> int:
    lower = " ".join(description.split()).lower()
    use_when_idx = lower.find("use when")
    tail = lower[use_when_idx + len("use when") :] if use_when_idx >= 0 else lower
    tokens = re.findall(r"[a-z0-9][a-z0-9+./-]*", tail)
    filtered = [tok for tok in tokens if len(tok) >= 3 and tok not in STOPWORDS]
    return len(set(filtered))


def audit_skill_doc(path: Path, root: Path) -> dict[str, Any]:
    rel = safe_rel(path, root)

    output: dict[str, Any] = {"file": rel, "status": "ok", "violations": [], "warnings": []}

    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        output["status"] = "violation"
        output["violations"].append(finding("read_error", f"Cannot read file as UTF-8: {exc}"))
        return output

    frontmatter, _frontmatter_text, body_text, fm_violations = parse_frontmatter(text)
    output["violations"].extend(fm_violations)

    if isinstance(frontmatter, dict):
        name = frontmatter.get("name")
        if not isinstance(name, str) or not name.strip():
            output["violations"].append(finding("name_missing", "Frontmatter requires non-empty string 'name'"))

        description = frontmatter.get("description")
        if not isinstance(description, str) or not description.strip():
            output["violations"].append(
                finding("description_missing", "Frontmatter requires non-empty string 'description'")
            )
        else:
            desc_norm = " ".join(description.split())
            if WORKFLOW_SUMMARY_RE.search(desc_norm):
                output["warnings"].append(
                    finding(
                        "description_workflow_summary",
                        "Description appears to summarize workflow/sequence; prefer trigger-only wording",
                    )
                )

            token_count = description_trigger_token_count(desc_norm)
            if token_count < 5:
                output["warnings"].append(
                    finding(
                        "description_keyword_coverage",
                        f"Description trigger keyword coverage appears sparse ({token_count} unique trigger tokens)",
                    )
                )

    windows_path = find_windows_style_path(text)
    if windows_path:
        output["violations"].append(
            finding("windows_path_detected", f"Windows-style path detected: {windows_path}")
        )

    body_line_count = len(body_text.splitlines())
    if body_line_count > 500:
        output["warnings"].append(
            finding(
                "skill_body_line_budget",
                f"SKILL.md body has {body_line_count} lines; recommended <= 500",
            )
        )

    level1_files: list[Path] = []
    for link in extract_md_links(path):
        target = (path.parent / link).resolve()
        if target.exists() and target.is_file():
            level1_files.append(target)

    nested_examples: list[str] = []
    for level1 in level1_files:
        for link in extract_md_links(level1):
            target = (level1.parent / link).resolve()
            if not target.exists() or not target.is_file():
                continue
            if target == path.resolve() or target in level1_files:
                continue
            nested_examples.append(
                f"{safe_rel(level1, root)} -> {link} -> {safe_rel(target, root)}"
            )

    if nested_examples:
        output["warnings"].append(
            finding(
                "nested_reference_depth",
                "Reference depth >1 hop from SKILL.md detected: " + "; ".join(nested_examples[:3]),
            )
        )

    if output["violations"]:
        output["status"] = "violation"

    return output


def render_human(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    summary = payload["summary"]
    violations = payload["violation_counts"]
    warnings = payload["warning_counts"]

    lines.append("Skill docs audit")
    lines.append(f"Files audited: {summary['total_files']}")
    lines.append(f"Files with violations: {summary['files_with_violations']}")
    lines.append(f"Total violations: {summary['total_violations']}")
    lines.append(f"Total warnings: {summary['total_warnings']}")
    lines.append("")

    if violations:
        lines.append("Violation counts:")
        for code, count in sorted(violations.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"  - {code}: {count}")
        lines.append("")

    if warnings:
        lines.append("Warning counts:")
        for code, count in sorted(warnings.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"  - {code}: {count}")
        lines.append("")

    lines.append("Per-file results:")
    for item in payload["files"]:
        lines.append(f"- {item['file']} [{item['status']}]")
        for v in item["violations"]:
            lines.append(f"    * {v['code']}: {v['detail']}")
        for w in item["warnings"]:
            lines.append(f"    ! {w['code']}: {w['detail']}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit SKILL.md documentation contracts")
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
        help="Optional explicit SKILL.md files to audit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()

    if args.files:
        files = [Path(f).resolve() if not Path(f).is_absolute() else Path(f) for f in args.files]
    else:
        files = discovered_skill_docs(root)

    results = [audit_skill_doc(path, root) for path in files]

    violation_counter: Counter[str] = Counter()
    warning_counter: Counter[str] = Counter()
    files_with_violations = 0
    total_violations = 0
    total_warnings = 0

    for item in results:
        if item["violations"]:
            files_with_violations += 1
            total_violations += len(item["violations"])
        total_warnings += len(item["warnings"])

        for v in item["violations"]:
            violation_counter[v["code"]] += 1
        for w in item["warnings"]:
            warning_counter[w["code"]] += 1

    payload = {
        "summary": {
            "total_files": len(results),
            "files_with_violations": files_with_violations,
            "total_violations": total_violations,
            "total_warnings": total_warnings,
        },
        "violation_counts": dict(violation_counter),
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
