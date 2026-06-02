# Changelog Template

## Purpose
Record each approved plan-patch operation during a refinement round. Append entries in reverse-chronological order.

## Entry format

```markdown
### Round N — YYYY-MM-DD

| # | Priority | Finding | Plan field | Action | Status |
|---|----------|---------|------------|--------|--------|
| 1 | P0 | {finding summary} | {field path} | {add/remove/replace} | applied |
| 2 | P1 | {finding summary} | {field path} | {add/remove/replace} | skipped |

**Reports consumed:**
- `{report-filename-1.html}`
- `{report-filename-2.html}`

**Patched outputs:**
- `.skill-plan.patch.yaml`
- `.skill-plan.patched.yaml`
```

## Rules

- One table per round.
- Mark each operation as `applied`, `skipped`, or `edited`.
- Append to existing changelog; do not overwrite prior rounds.
