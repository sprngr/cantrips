# Priority Rules — Finding Severity Tiers

## Purpose
Read at step 5. Classify findings from skill-check and skill-eval reports into priority tiers for ranked processing.

## Tiers

| Tier | Label | Source | Examples |
|------|-------|--------|----------|
| P0 | Spec violation | skill-check `spec.checks[]` where `pass: false` | Missing frontmatter `name`, `description` exceeds 1024 chars, unknown fields |
| P1 | Failing eval | skill-eval `evals[].assertions[]` where `pass: false` | Assertion failure, pass rate < 0.5, skill-dependent failure |
| P2 | Best-practice warning | skill-check `best_practices.warnings[]` | No working example, no progressive disclosure, generic content |
| P3 | Style nit | skill-check `structure.warnings[]`, skill-eval `patterns[]` | Missing `references/` directory, inconsistent naming, wasted tokens |

## Ranking within tier

1. **P0**: Order by spec section number (lower = more fundamental).
2. **P1**: Order by assertion failure count descending, then by eval id alphabetically.
3. **P2**: Order by best-practice category: grounding > content quality > instruction design > token efficiency.
4. **P3**: Order by estimated fix effort ascending (quick wins first).

## Cross-report deduplication

- Match findings across skill-check and skill-eval by affected plan area (intent, scope, mechanism, workflow_notes, etc.).
- Merge duplicates. Keep highest priority tier.
- Annotate merged findings with both source report paths.

## Queue output format

Present to user as numbered list:

```
[1] P0 — spec: name_matches_dir — name 'foo' does not match directory 'bar'
[2] P1 — eval: test-03 — assertion "output contains header" FAIL
[3] P2 — bp: no working example included
[4] P3 — struct: missing references/ directory
```
