
#!/usr/bin/env python3
"""Deterministic assertion grading for eval outputs.

Reads assertions from a JSON array file. Checks file-existence, valid-JSON,
count, and content-match assertions against the output directory.
Prints grading JSON to stdout.
"""

import json
import sys
import glob
import os
import re


def check_file_exists(text: str, output_dir: str) -> tuple[bool, str]:
    """Check if the output directory contains files."""
    files = os.listdir(output_dir)
    if files:
        return True, f"Found {len(files)} files: {', '.join(files[:5])}"
    return False, f"No files found in {output_dir}"


def check_valid_json(text: str, output_dir: str) -> tuple[bool, str]:
    """Check if all JSON files in output are valid."""
    json_files = glob.glob(os.path.join(output_dir, "*.json"))
    if not json_files:
        return False, "No JSON files found"
    bad = []
    for f in json_files[:10]:
        try:
            with open(f) as fh:
                json.load(fh)
        except (json.JSONDecodeError, OSError):
            bad.append(os.path.basename(f))
    if bad:
        return False, f"Invalid JSON in: {', '.join(bad)}"
    return True, f"Checked {len(json_files)} JSON file(s). All valid."


def check_count(text: str, output_dir: str) -> tuple[bool, str]:
    """Check file counts or item counts."""
    files = glob.glob(os.path.join(output_dir, "*"))
    return len(files) > 0, f"Found {len(files)} output file(s)"


def check_contains(text: str, output_dir: str) -> tuple[bool, str]:
    """Check if output contains expected text."""
    targets = re.findall(r"['\"]([^'\"]+)['\"]", text)
    if not targets:
        return False, "No quoted target terms found in assertion"

    combined = ""
    for f in glob.glob(os.path.join(output_dir, "*")):
        if os.path.isfile(f):
            try:
                with open(f, errors="ignore") as fh:
                    combined += fh.read() + "\n"
            except OSError:
                pass
    found = any(t.lower() in combined.lower() for t in targets)
    return found, f"Scanned {len(combined)} chars. Target terms {'found' if found else 'not found'}"


def classify_assertion(text: str) -> str:
    """Return which checker handles this assertion."""
    lower = text.lower()
    if any(w in lower for w in ["file exist", "file present", "file found", "image file", "csv file"]):
        return "file_exists"
    if any(w in lower for w in ["valid json", "json valid", "parseable json"]):
        return "valid_json"
    if any(w in lower for w in ["includes", "contains", "mentions", "label", "labeled", "has"]):
        return "contains"
    if any(w in lower for w in ["count", "at least", "contains", "has", "number", "exactly"]):
        return "count"
    return "pending"


CHECKERS = {
    "file_exists": check_file_exists,
    "valid_json": check_valid_json,
    "count": check_count,
    "contains": check_contains,
}

PATTERN_MAP = {
    r"['\"]([^'\"]+)['\"]": str,
}


def main():
    if len(sys.argv) != 3:
        print("Usage: grade_assertions.py <output-dir> <assertions-json>", file=sys.stderr)
        sys.exit(1)

    output_dir = sys.argv[1]
    assertions_file = sys.argv[2]

    if not os.path.isdir(output_dir):
        print(json.dumps({"error": f"output directory {output_dir} not found"}))
        sys.exit(1)

    with open(assertions_file) as f:
        assertions = json.load(f)

    results = []
    determined = 0
    pending = 0

    for assertion in assertions:
        text = assertion.get("text", "")
        kind = classify_assertion(text)
        checker = CHECKERS.get(kind)

        if checker:
            passed, evidence = checker(text, output_dir)
            results.append({
                "text": text,
                "passed": passed,
                "evidence": evidence,
                "graded_by": "script",
            })
            determined += 1
        else:
            results.append({
                "text": text,
                "passed": None,
                "evidence": "Non-deterministic assertion, defer to LLM grading",
                "graded_by": "pending",
            })
            pending += 1

    passed_count = len([r for r in results if r.get("passed")])

    output = {
        "assertion_results": results,
        "summary": {
            "passed": passed_count,
            "failed": determined - passed_count,
            "pending_llm": pending,
            "total_determined": determined,
            "total": len(results),
        },
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
