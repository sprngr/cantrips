# Plan Patch Proposal Format

## Purpose

Read at workflow step 10. Format each plan patch proposal consistently for user review.

## Template

```
┌── Plan Patch Proposal #N ─────────────────────────────
│ Priority: P{0-3} — {tier label}
│ Source:   {report type} → {finding id}
│ Finding:  {one-line description of the problem}
│
│ Plan field: {intent|scope|mechanism|context_assets|workflow_notes|example_placed|target_path}
│ Action:     {add | remove | replace}
│
│ Before:
│   {existing value from .skill-plan.yaml}
│
│ After:
│   {proposed patched value}
│
│ Rationale: {why this patch resolves the finding}
└───────────────────────────────────────────────────────
[apply / skip / edit / stop]
```

## Rules

- Show exactly one proposal at a time.
- Proposal must target plan fields only. No direct skill bundle file edits.
- Include both `Before` and `After` values for `replace` actions.
- For `add` actions, `Before` may be `null`.
- For `remove` actions, `After` may be `null`.
- On `edit`, accept user's modified `After` and re-present once for confirmation.
- Keep each proposal scoped to one field change (one concern per patch operation).
