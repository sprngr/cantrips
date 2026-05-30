# ADR-0003: `skill-eval` JSON Summary Contract

- **Status:** Proposed
- **Date:** 2026-05-30
- **Deciders:** Repository maintainers
- **Related:** ADR-0001, SDLC Issues #6 and #7

## Context

`skill-eval` emits machine-readable summary JSON inside HTML reports. Downstream tooling (`skill-refine`, roll-up dashboards, CI analyzers) depends on this contract.

Current risk:
- field naming drift (`time` vs `time_seconds` variants)
- flexible `iteration` representations
- schema and report output may diverge over time

Need stable contract with explicit compatibility rules.

## Decision

Standardize `skill-eval` `{{JSON_SUMMARY}}` payload and enforce via schema validation in CI/tests.

## Canonical Payload (v1)

Required top-level fields:
- `skill` (string)
- `iteration` (string, pattern `iteration-N`)
- `report_date` (ISO-like date string)
- `eval_count` (integer)
- `with_skill` (object)
- `without_skill` (object)

Recommended fields:
- `readiness` `{ score, total, band }`
- `delta` `{ pass_rate, tokens, time }`
- `evals[]`
- `patterns[]`
- `fixes[]`

Metric subobject contract (`with_skill`, `without_skill`):
- `pass_rate` (number)
- `stddev` (number)
- `samples` (integer)
- `tokens` (number)
- `time` (number, seconds)

## Compatibility Policy

1. Additive fields allowed.
2. Renaming/removal of existing fields is breaking and requires:
   - new ADR
   - schema version bump
   - migration note in changelog.
3. Prefer `iteration` as `iteration-N` string for consistency.

## Serialization/Placement Rule

- JSON summary must be embedded in dedicated machine block near top of report template.
- Parsing should target machine block explicitly (not positional first-`<pre>` assumption).

## Consequences

### Positive
- Deterministic downstream parsing and dashboarding
- Reduced parser fragility
- Easier CI contract testing

### Negative
- Slight overhead when evolving report structure

## Implementation Notes

1. Align `skill-eval` report writer output to this contract.
2. Keep `skills/meta-skills/skill-refine/assets/report-schema.json` synchronized.
3. Add/maintain tests for accepted payload examples.
4. Document contract in `skill-eval/SKILL.md` references section.

## Verification

- Sample output validates against schema.
- `skill-refine` parser tests include multi-template payload extraction.
- Roll-up script consumes payload without ad-hoc fallbacks.
