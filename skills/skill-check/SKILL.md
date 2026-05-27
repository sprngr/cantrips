---
name: skill-check
description: Audit and validate agent skills against the agentskills.io specification,
  best practices, eval procedure, and skills-ref implementation. Use when "audit skill",
  "validate skill", "skill quality review", or "skill check".
---
# Skill Check

Audit agent skills for spec compliance, best-practice adherence, and quality.

## Quick start

```bash
scripts/validate-structure.sh path/to/target-skill
```

## Workflows

1. Read target `SKILL.md`. Extract frontmatter YAML and body content.
2. Run `scripts/validate-structure.sh <skill-path>`. Capture pass/fail output.
3. Read `references/spec-requirements.md`. Check frontmatter against each spec rule.
4. Read `references/best-practices.md`. Evaluate body against each best-practice guideline.
5. Read `references/eval-checklist.md`. Score eval setup quality.
6. Run `scripts/compare-structure.sh <skill-path>`. Output structural diff vs. skills-ref patterns.
7. Produce HTML report with styled sections: summary score, spec compliance table, best-practice warnings list, structure comparison, and actionable fix suggestions.
8. Write report to `<skill-path>/skill-check-report.html`.

## Reference files

See [spec-requirements.md](references/spec-requirements.md) for all spec clauses.
See [best-practices.md](references/best-practices.md) for quality guidelines.
See [eval-checklist.md](references/eval-checklist.md) for eval setup scorecard.
See [skills-ref-patterns.md](references/skills-ref-patterns.md) for structural patterns.
