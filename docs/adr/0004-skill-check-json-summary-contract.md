# ADR-0004: `skill-check` JSON Summary Contract

- **Status:** Accepted
- **Date:** 2026-05-30
- **Deciders:** Repository maintainers
- **Related:** ADR-0001, SDLC Issues #4 and #7

## Context

`skill-check` reports include a machine-readable JSON summary consumed by `skill-refine` and future portfolio roll-ups.

Risk:
- structural score type inconsistency (string/int variants)
- optional sections interpreted differently by downstream tools
- report template edits can silently break parsers

Need explicit stable contract.

## Decision

Adopt a canonical `skill-check` JSON summary schema and compatibility policy.

## Canonical Payload (v1)

Required top-level fields:
- `skill` (string)
- `target_path` (string)
- `audit_date` (string)
- `grade` (string, regex `^[ABCDF][+-]?$`)
- `spec` (object)
- `best_practices` (object)
- `structure` (object)

`spec` object:
- `score` (integer)
- `total` (integer)
- `checks[]` with `{check, pass, detail}`

`best_practices` object:
- `score` (integer)
- `total` (integer)
- `warnings[]` (string array)

`structure` object:
- `score` (integer preferred; string tolerated for backward compatibility)
- `found[]` (optional)
- `warnings[]` (optional)

Optional top-level fields:
- `has_evals` (boolean)
- `fixes[]` with `{priority, description}`

## Compatibility Policy

1. Additive fields allowed.
2. Existing required fields cannot be removed or renamed without:
   - new ADR
   - schema bump
   - migration guidance.
3. `structure.score` string support is temporary legacy compatibility; target steady-state integer only.

## Serialization/Placement Rule

- Machine JSON summary must remain in explicit machine section near top of report.
- Downstream parser anchors to machine section marker, not first generic `<pre>` block.
- Enforcement policy:
  - `skill-check` payload extraction is machine-block strict (`details#machine-report` required).
  - generic `<pre>` fallback is not accepted for `skill-check` report parsing.
  - fallback remains available for non-`skill-check` report types for legacy tolerance.

## Consequences

### Positive
- Reliable parsing for refinement and reporting workflows
- Fewer false failures from formatting/template edits

### Negative
- Requires schema discipline when evolving report content

## Implementation Notes

1. Keep template variables and emitted payload aligned (`skill-check` generation step).
2. Keep `skills/meta-skills/skill-refine/assets/report-schema.json` synchronized.
3. Add regression tests for parser against representative report variants.
4. Track legacy compatibility cleanup for `structure.score` type.
5. Follow implementation checklist in `docs/adr/0004-implementation-plan.md`.

## Contract Source of Truth

- Schema: `skills/meta-skills/skill-refine/assets/report-schema.json`
- Report template embedding `{{JSON_SUMMARY}}`: `skills/meta-skills/skill-check/assets/skill-check-report-template.html`
- Parser and contract regression tests: `skills/meta-skills/skill-refine/scripts/tests/test_parse_report.py`

## Verification

- Generated `*-skill-check-report.html` payload validates against schema.
- Parser tests pass for canonical and legacy-compatible examples.
- Roll-up script consumes payload with no custom per-skill exceptions.

## Completion Note (2026-05-30)

- Task 1 baseline completed (`docs/reports/adr-0004-contract-baseline.md`).
- Task 2 schema tightening completed:
  - `spec.checks[]` requires `detail`
  - `best_practices` requires `warnings`
  - `fixes[]` items require `priority` + `description`
- Task 3 parser hardening completed:
  - machine-block strict extraction for `skill-check`
  - fallback retained for non-`skill-check` report types
- Task 5 verification completed (`docs/reports/adr-0004-pr-evidence.md`).
