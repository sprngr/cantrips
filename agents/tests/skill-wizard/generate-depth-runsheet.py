#!/usr/bin/env python3
"""Generate manual test run sheet for skill-wizard depth selection behavior."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Scenario:
    case_id: str
    title: str
    prompt: str
    expected: list[str]
    notes: list[str]


SCENARIOS: list[Scenario] = [
    Scenario(
        case_id="SW-D01",
        title="Quick recommendation for simple single-output intent",
        prompt='Build a simple commit message helper skill. One action, one output.',
        expected=[
            'First response asks exactly one question with recommendation form: "Recommend quick ... Choose mode: quick or deep."',
            "No stacked second question in same turn.",
        ],
        notes=[
            "Signal profile: quick-skewed (single/simple/one output).",
        ],
    ),
    Scenario(
        case_id="SW-D02",
        title="Deep recommendation for orchestration-heavy intent",
        prompt=(
            "Plan a CI/CD orchestration skill with staged approvals, rollback, "
            "multi-role handoffs, and compliance checkpoints."
        ),
        expected=[
            'First response asks exactly one question with recommendation form: "Recommend deep ... Choose mode: quick or deep."',
            "No stacked second question in same turn.",
        ],
        notes=[
            "Signal profile: deep-skewed (orchestration/multi-role/compliance).",
        ],
    ),
    Scenario(
        case_id="SW-D03",
        title="Neutral fallback for mixed/unclear signals",
        prompt="Help me design a planning helper. Could stay simple, might evolve into pipeline later.",
        expected=[
            'First response asks exactly one neutral question: "Pick planning mode: quick (3-4 turns) or deep (dynamic)?"',
            "No recommendation phrase when signals are mixed.",
        ],
        notes=[
            "Signal profile: mixed/ambiguous.",
        ],
    ),
    Scenario(
        case_id="SW-D04",
        title="Honor explicit user depth (deep)",
        prompt="Deep mode: build a single-file formatter skill.",
        expected=[
            "Depth is honored directly; no depth-selection question required.",
            "Flow proceeds into deep interview behavior.",
        ],
        notes=[
            "Explicit depth from user must override heuristic recommendation flow.",
        ],
    ),
    Scenario(
        case_id="SW-D05",
        title="User override after recommendation",
        prompt="Create simple changelog tidy skill for one output file.",
        expected=[
            "First response recommends quick and asks user to choose quick/deep.",
            "After user reply `deep`, agent proceeds with deep interview path without resistance.",
        ],
        notes=[
            "Manual step: send second message exactly `deep`.",
        ],
    ),
    Scenario(
        case_id="SW-D06",
        title="Resume path bypasses depth selection",
        prompt="Continue plan",
        expected=[
            "With fixture `.skill-plan.yaml` (`completed: false`) present, first response resumes unresolved branch.",
            "No State 0.5 depth question appears.",
        ],
        notes=[
            "Setup: copy fixtures/resume-incomplete.skill-plan.yaml to working directory as `.skill-plan.yaml`.",
        ],
    ),
]


def build_runsheet() -> str:
    lines: list[str] = []
    lines.append("# Skill Wizard Depth Selection - Manual Run Sheet")
    lines.append("")
    lines.append("Use with checklist: `agents/tests/skill-wizard/depth-checklist.md`")
    lines.append("")
    lines.append("## Result summary")
    lines.append("")
    lines.append("- [ ] SW-D01")
    lines.append("- [ ] SW-D02")
    lines.append("- [ ] SW-D03")
    lines.append("- [ ] SW-D04")
    lines.append("- [ ] SW-D05")
    lines.append("- [ ] SW-D06")
    lines.append("")

    for scenario in SCENARIOS:
        lines.append(f"## {scenario.case_id} - {scenario.title}")
        lines.append("")
        lines.append("### Prompt")
        lines.append("")
        lines.append("```text")
        lines.append(scenario.prompt)
        lines.append("```")
        lines.append("")
        lines.append("### Expected")
        lines.append("")
        for item in scenario.expected:
            lines.append(f"- [ ] {item}")
        lines.append("")
        lines.append("### Notes")
        lines.append("")
        for note in scenario.notes:
            lines.append(f"- {note}")
        lines.append("")
        lines.append("### Observed first response")
        lines.append("")
        lines.append("```text")
        lines.append("<paste assistant response>")
        lines.append("```")
        lines.append("")
        lines.append("### Verdict")
        lines.append("")
        lines.append("- Pass / Fail:")
        lines.append("- Follow-up:")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate manual run sheet for skill-wizard depth tests"
    )
    parser.add_argument(
        "--output",
        default="agents/tests/skill-wizard/depth-runsheet.md",
        help="Output markdown path (default: agents/tests/skill-wizard/depth-runsheet.md)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_runsheet(), encoding="utf-8")
    print(f"Wrote run sheet: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
