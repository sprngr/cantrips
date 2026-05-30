#!/usr/bin/env python3
"""Extract JSON summary block from skill-check or skill-eval HTML reports.

Primary extraction targets machine-report block (details#machine-report > pre)
to avoid selecting unrelated <pre> content. Includes legacy-tolerant fallback
to first parseable <pre> JSON when machine block is missing.
"""

import json
import re
import sys
import os
import html


def _extract_pre_blocks(html_text: str) -> list[str]:
    return re.findall(r"<pre[^>]*>(.*?)</pre>", html_text, re.DOTALL)


def _parse_json_block(raw_block: str) -> dict | None:
    raw = html.unescape(raw_block.strip())
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def extract_json_with_mode(html_text: str) -> tuple[dict | None, str]:
    """Extract JSON summary and return extraction mode.

    Modes:
    - machine: parsed from details#machine-report pre block
    - fallback: parsed from first parseable <pre> block
    - none: no parseable JSON block found
    """
    machine_match = re.search(
        r"<details[^>]*id=[\"']machine-report[\"'][^>]*>.*?<pre[^>]*>(.*?)</pre>.*?</details>",
        html_text,
        re.DOTALL,
    )
    if machine_match:
        data = _parse_json_block(machine_match.group(1))
        if data is not None:
            return data, "machine"

    # Legacy fallback: first parseable JSON <pre>
    for block in _extract_pre_blocks(html_text):
        data = _parse_json_block(block)
        if data is not None:
            return data, "fallback"

    return None, "none"


def extract_json_from_html(html_text: str) -> dict | None:
    """Backward-compatible extractor returning only parsed JSON (if any)."""
    data, _ = extract_json_with_mode(html_text)
    return data


def detect_report_type(data: dict) -> str:
    """Return 'skill-check' or 'skill-eval' based on JSON keys."""
    if "spec" in data and "best_practices" in data:
        return "skill-check"
    if "with_skill" in data and "without_skill" in data:
        return "skill-eval"
    return "unknown"


def flatten_findings(data: dict, report_type: str) -> list[dict]:
    """Extract individual findings from parsed report JSON."""
    findings = []

    if report_type == "skill-check":
        # Spec check failures
        for check in data.get("spec", {}).get("checks", []):
            if not check.get("pass"):
                findings.append({
                    "source": "spec",
                    "check": check.get("check", ""),
                    "detail": check.get("detail", ""),
                })
        # Best practice warnings
        for warning in data.get("best_practices", {}).get("warnings", []):
            findings.append({
                "source": "best_practice",
                "check": "warning",
                "detail": warning,
            })
        # Structure warnings
        for warning in data.get("structure", {}).get("warnings", []):
            findings.append({
                "source": "structure",
                "check": "warning",
                "detail": warning,
            })
        # Suggested fixes
        for fix in data.get("fixes", []):
            findings.append({
                "source": "fix",
                "check": fix.get("priority", ""),
                "detail": fix.get("description", ""),
            })

    elif report_type == "skill-eval":
        # Failed assertions
        for ev in data.get("evals", []):
            for assertion in ev.get("assertions", []):
                if not assertion.get("pass"):
                    findings.append({
                        "source": "eval",
                        "check": ev.get("id", ""),
                        "detail": assertion.get("evidence", ""),
                    })
        # Patterns
        for pattern in data.get("patterns", []):
            findings.append({
                "source": "pattern",
                "check": pattern.get("type", ""),
                "detail": pattern.get("action", ""),
            })
        # Fixes
        for fix in data.get("fixes", []):
            findings.append({
                "source": "fix",
                "check": fix.get("priority", ""),
                "detail": fix.get("description", ""),
            })

    return findings


def main():
    if len(sys.argv) != 2:
        print("Usage: parse_report.py <report-html-path>", file=sys.stderr)
        sys.exit(1)

    report_path = sys.argv[1]
    if not os.path.isfile(report_path):
        print(json.dumps({"error": f"File not found: {report_path}"}))
        sys.exit(1)

    with open(report_path, "r", encoding="utf-8") as f:
        html_text = f.read()

    data, extraction_mode = extract_json_with_mode(html_text)
    if data is None:
        print(json.dumps({"error": "No JSON summary found in <pre> block"}))
        sys.exit(1)

    report_type = detect_report_type(data)
    findings = flatten_findings(data, report_type)

    output = {
        "report_type": report_type,
        "extraction_mode": extraction_mode,
        "report_path": report_path,
        "raw_summary": data,
        "findings": findings,
        "finding_count": len(findings),
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
