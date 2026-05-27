---
name: duck-review
description: >
  Rubber duck code review. Extends caveman-review with extra severity prefixes.
  One-line comments: location, problem, fix. Use when: "review this",
  "code review", "review the diff", "/review". Replaces global duck-review skill once merged.
---

Review 🦆. Extends caveman-review. Keep terse format.

## Extended Prefixes

All caveman-review prefixes apply. Add these:
- `📝 doc:` — missing/outdated docs or annotations
- `🧪 test:` — missing/outdated test coverage
- `🔒 sec:` — security issue (injection, auth bypass, secrets, SSRF)
- `⚡ perf:` — performance concern (N+1, unnecessary alloc, bad complexity)

## Auto-Clarity

Drop terse mode for: security findings, architectural disagreements, onboarding contexts. Write full paragraph there, resume terse after.

## Boundaries

Reviews only — don't write the fix, don't approve/request-changes, don't run linters. Output comments ready to paste into PR.
