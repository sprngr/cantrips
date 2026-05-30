# ADR-0004 Contract Baseline (Task 1)

- **Date:** 2026-05-30
- **Scope:** `skill-check` JSON summary contract inventory and mismatch analysis
- **Sources reviewed:**
  - `skills/meta-skills/skill-check/assets/skill-check-report-template.html`
  - `skills/meta-skills/skill-refine/assets/report-schema.json` (`skill-check-report` definition)
  - emitted samples:
    - `skills/experimental/goblin-mode/goblin-mode-skill-check-report.html`
    - `skills/experimental/squash/squash-skill-check-report.html`
  - contract: `docs/adr/0004-skill-check-json-summary-contract.md`

## ADR-0004 Required Contract (reference)

Required top-level fields:
- `skill`, `target_path`, `audit_date`, `grade`, `spec`, `best_practices`, `structure`

Required nested structure:
- `spec`: `score`, `total`, `checks[]` with `{check, pass, detail}`
- `best_practices`: `score`, `total`, `warnings[]`
- `structure`: `score` (integer canonical, string tolerated for legacy), optional `found[]`, `warnings[]`

Optional top-level fields:
- `has_evals`
- `fixes[]` with `{priority, description}`

## Findings

### 1) Template placement
- **Status:** ✅ aligned
- Machine JSON summary is embedded in explicit machine section near top:
  - `<details id="machine-report"> ... <pre>{{JSON_SUMMARY}}</pre>`

### 2) Emitted sample payloads
- **Status:** ✅ mostly aligned
- Both reviewed samples include required top-level fields and expected nested sections.
- `structure.score` is integer in both samples (canonical path), while schema still permits string for legacy compatibility.

### 3) Schema enforcement gaps vs ADR-0004
- **Status:** ⚠️ partially aligned (under-enforced in some nested item requirements)

## Mismatch Matrix

| Area | ADR-0004 expectation | Current schema | Impact | Priority |
|---|---|---|---|---|
| `spec.checks[]` item keys | `{check, pass, detail}` expected | `detail` not required | allows incomplete check records | P1 |
| `best_practices.warnings` | `warnings[]` expected | `warnings` optional | allows payloads without warning array | P2 |
| `fixes[]` item keys | `{priority, description}` expected when present | both keys optional | allows weakly-shaped fix objects | P2 |

## Notes

- `structure.score` int/string support is intentionally compatible with ADR-0004 legacy policy (no mismatch).
- Sample report `target_path` values still reference pre-experimental paths (`skills/squash`, `skills/goblin-mode`); this is content staleness, not schema contract break.

## Recommendations for Task 2

1. Tighten `skill-check-report.spec.checks[].required` to include `detail`.
2. Require `best_practices.warnings` in `best_practices.required`.
3. Keep `fixes` optional top-level, but require `priority` + `description` when a fix item exists.
4. Retain `structure.score` int/string compatibility until explicit legacy removal ADR.

## Task 1 Exit

- [x] Template reviewed
- [x] Schema reviewed
- [x] Emitted samples reviewed
- [x] Mismatch baseline captured
