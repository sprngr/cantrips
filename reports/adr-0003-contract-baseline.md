# ADR-0003 Contract Baseline (Task 1)

- **Date:** 2026-05-30
- **Scope:** `skill-eval` JSON summary contract inventory and mismatch check
- **Sources reviewed:**
  - `skills/meta-skills/skill-eval/assets/eval-report-template.html`
  - `skills/meta-skills/skill-refine/assets/report-schema.json`
  - sample emitted report JSON: `skills/experimental/squash/squash-iteration-5-eval-report.html`
  - contract text: `docs/adr/0003-skill-eval-json-summary-contract.md`

## ADR-0003 Required Contract (reference)

Required top-level keys:
- `skill` (string)
- `iteration` (`iteration-N` string)
- `report_date` (string)
- `eval_count` (integer)
- `with_skill` (object)
- `without_skill` (object)

Metric object (`with_skill`, `without_skill`) required keys:
- `pass_rate` (number)
- `stddev` (number)
- `samples` (integer)
- `tokens` (number)
- `time` (number, seconds)

## Current State Findings

### 1) Template placement
- **Status:** ✅ aligned
- `eval-report-template.html` includes `{{JSON_SUMMARY}}` in dedicated machine block near top.

### 2) Sample emitted payload shape
- **Status:** ✅ aligned
- Sample `squash-iteration-5-eval-report.html` JSON has:
  - required top-level keys
  - `iteration` as `"iteration-5"`
  - metric objects using `time` (seconds)

### 3) Schema compatibility (`report-schema.json`)
- **Status:** ⚠️ partially aligned / too permissive in one area
- `skill-eval-report.iteration` currently allows:
  - integer
  - string `iteration-N`
- ADR-0003 prefers canonical `iteration-N` string.

## Mismatch Summary

| Area | Expected | Current | Impact | Priority |
|---|---|---|---|---|
| `iteration` type in schema | string `iteration-N` | `integer` OR string | allows non-canonical payloads | P1 |

No other mismatches identified in Task 1 review.

## Recommendations for Task 2

1. Tighten `skill-eval-report.iteration` schema to string pattern `^iteration-[0-9]+$` only.
2. Keep parser tolerant for legacy inputs (read compatibility), but enforce canonical write contract at schema/report generation boundary.
3. Add explicit tests proving:
   - canonical string accepted
   - integer iteration rejected by strict contract tests (or flagged as legacy compatibility case if intentionally retained).

## Task 1 Exit

- [x] Reviewed template
- [x] Reviewed sample emitted JSON summary
- [x] Reviewed schema definition
- [x] Recorded mismatch baseline for Task 2
