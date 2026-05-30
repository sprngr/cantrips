# ADR-0004: `skill-check` JSON Summary Contract

- **Status:** Proposed
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
- Downstream parser should anchor to machine section marker, not first generic `<pre>` block.

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

## Verification

- Generated `*-skill-check-report.html` payload validates against schema.
- Parser tests pass for canonical and legacy-compatible examples.
- Roll-up script consumes payload with no custom per-skill exceptions.
