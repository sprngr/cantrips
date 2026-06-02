---
name: skill-refine
description: >
  Use when `.skill-plan.yaml` exists and skill-check/skill-eval feedback should
  be converted into patch operations before rerunning /skill-forge.
---
# Skill Refine

Convert feedback into plan-level patches. Do not edit the skill bundle directly.

## Quick start

```
Agent: "refine plan skills/my-skill/.skill-plan.yaml"
```

## Workflows

### 1. Load plan + reports

1. Require existing `.skill-plan.yaml` path. If missing, stop and ask user for path.
2. Read base plan YAML. Confirm it is parseable and has required planning fields.
3. Locate `*-skill-check-report.html` and/or `*-eval-report.html` provided by user.
4. Run `Bash scripts/parse-report.sh <report-path>` for each report.
5. Validate parsed JSON against `assets/report-schema.json`. Show parse errors if malformed.
6. Present feedback summary: total findings, top failures, affected plan areas.

### 2. Rank findings

7. Read `references/priority-rules.md` and classify findings into P0-P3.
8. Sort findings by tier, then impact within tier.
9. Present ranked queue to user. Include counts per priority tier.

### 3. Propose plan patch operations

10. For top-ranked finding, generate one plan patch proposal using `references/change-proposal-format.md`.
11. Scope patches to plan fields only (e.g., `intent`, `scope`, `mechanism`, `context_assets`, `workflow_notes`, `example_placed`, `target_path`).
12. Present options: `[apply / skip / edit / stop]`.
13. On `apply`, append operation to patch queue.
14. On `edit`, accept user's modified patch operation and re-present once for confirmation.
15. On `skip`, advance to next finding. On `stop`, persist queue and exit loop.

### 4. Build artifacts

16. Write queued operations to `<plan-dir>/.skill-plan.patch.yaml` using `assets/plan-patch-template.yaml` shape.
17. Apply operations to base plan in memory and produce `<plan-dir>/.skill-plan.patched.yaml`.
18. Run `Bash scripts/validate-plan.sh <plan-dir>/.skill-plan.patched.yaml` to validate forge import contract.
19. If validation fails, mark failing operations and ask user whether to edit/drop them.
20. On validation pass, show concise plan diff summary (changed fields only).

### 5. Handoff

21. Ask user to approve patched plan for forge input.
22. On approval, instruct: `/skill-forge <plan-dir>/.skill-plan.patched.yaml`.
23. On reject, keep patch artifact and return to step 10.

## Guardrails

- Human-in-the-loop always. Never auto-apply patches without explicit user approval.
- Never edit target skill bundle files directly in this skill.
- Keep patch operations granular (one concern per operation).
- Preserve original `.skill-plan.yaml`; patched output goes to `.skill-plan.patched.yaml`.

## Reference files

See [priority-rules.md](references/priority-rules.md) for finding severity tiers and ranking logic.
See [change-proposal-format.md](references/change-proposal-format.md) for patch proposal template.
See [Example.md](references/Example.md) for end-to-end walkthrough.
See [report-schema.json](assets/report-schema.json) for parsed report JSON schema.
See [plan-patch-template.yaml](assets/plan-patch-template.yaml) for patch artifact shape.
See [changelog-template.md](assets/changelog-template.md) for patch log entry format.
