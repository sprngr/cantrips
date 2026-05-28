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
7. Read `assets/skill-check-report-template.html` (templatized HTML report). Fill template variables with audit data:
   - `{{SKILL_NAME}}`, `{{TARGET_PATH}}`, `{{AUDIT_DATE}}`
   - `{{SPEC_SCORE}}`, `{{SPEC_PCT}}`, `{{SPEC_CLASS}}`, `{{SPEC_SUBTITLE}}`
   - `{{BP_SCORE}}`, `{{BP_PCT}}`, `{{BP_CLASS}}`, `{{BP_SUBTITLE}}`
   - `{{EVAL_SCORE}}`, `{{EVAL_PCT}}`, `{{EVAL_CLASS}}`, `{{EVAL_SUBTITLE}}`, `{{EVAL_NOTES}}`
   - `{{STRUCT_SCORE}}`, `{{STRUCT_CLASS}}`, `{{STRUCT_SUBTITLE}}`
   - `{{SPEC_ROWS}}`, `{{BP_ROWS}}`, `{{EVAL_ROWS}}`, `{{STRUCT_ROWS}}` (table `<tr>` blocks)
   - `{{BP_WARNINGS}}` (warning `<li>` blocks), `{{FIXES}}` (fix `<li>` blocks)
   - `{{GRADE}}`, `{{GRADE_CLASS}}`, `{{VERDICT_TEXT}}`
   - `{{JSON_SUMMARY}}` — compact JSON object with all scores, pass/fail per check, and machine-parseable structure. Embed in `<pre>` block at top so downstream skills can read just the first ~30 lines for machine data. JSON schema:
     ```
     { skill, target_path, audit_date, grade,
       spec: { score, total, checks: [{check, pass, detail}] },
       best_practices: { score, total, warnings: [string] },
       eval_readiness: { score, total, items: [{item, pass}] },
       structure: { score, found: [string], warnings: [string] },
       fixes: [{priority, description}]
     }
     ```
8. Write filled report to `<skill-path>/skill-check-report.html`.

## Reference files

See [spec-requirements.md](references/spec-requirements.md) for all spec clauses.
See [best-practices.md](references/best-practices.md) for quality guidelines.
See [eval-checklist.md](references/eval-checklist.md) for eval setup scorecard.
See [skills-ref-patterns.md](references/skills-ref-patterns.md) for structural patterns.
See [skill-check-report.html](assets/skill-check-report.html) for the templatized HTML report (use in step 7).
