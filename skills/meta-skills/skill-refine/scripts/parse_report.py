#!/usr/bin/env python3
"""Extract JSON summary block from skill-check or skill-eval HTML reports.

Reads the first <pre> tag in the report (which contains the {{JSON_SUMMARY}})
and outputs parsed JSON to stdout. Detects report type (skill-check vs eval)
from the JSON keys.
"""

import json
import re
import sys
import os


def extract_json_from_html(html: str) -> dict | None:
    """Find first <pre> block and parse its JSON content."""
    match = re.search(r"<pre[^>]*>(.*?)</pre>", html, re.DOTALL)
    if not match:
        return None
    raw = match.group(1).strip()
    # Strip HTML entities
    raw = raw.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


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

    with open(report_path, errors="ignore") as f:
        html = f.read()

    data = extract_json_from_html(html)
    if data is None:
        print(json.dumps({"error": "No JSON summary found in <pre> block"}))
        sys.exit(1)

    report_type = detect_report_type(data)
    findings = flatten_findings(data, report_type)

    output = {
        "report_type": report_type,
        "report_path": report_path,
        "raw_summary": data,
        "findings": findings,
        "finding_count": len(findings),
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
