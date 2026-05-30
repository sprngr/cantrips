# ADR-0004 Implementation Plan: `skill-check` JSON Summary Contract

- **Status:** Draft
- **Date:** 2026-05-30
- **Owner:** Repository maintainers
- **Parent ADR:** [ADR-0004](./0004-skill-check-json-summary-contract.md)
- **Execution PR:** Next ADR execution PR after ADR-0003

## Objective

Stabilize `skill-check` machine-readable JSON summary contract so report output, schema validation, parser extraction, and downstream tooling remain consistent and deterministic.

## Scope

### In Scope
- Inventory current `skill-check` JSON summary output vs ADR-0004 contract
- Align `report-schema.json` skill-check definition where needed
- Add parser/schema regression tests for canonical + legacy-compatible cases
- Document source-of-truth and completion evidence

### Out of Scope
- `skill-eval` contract changes (already addressed by ADR-0003)
- full portfolio roll-up implementation

## Definition of Done (Execution)

- [ ] `skill-check` JSON summary required top-level fields validated by schema
- [ ] `spec` and `best_practices` required subkeys enforced
- [ ] `structure.score` compatibility behavior explicit (int canonical, string legacy tolerated)
- [ ] parser tests cover machine-block and fallback extraction behavior for skill-check payloads
- [ ] docs and ADR references aligned to active contract paths
- [ ] evidence report produced

## Work Breakdown (Task-Level)

### Task 1 — Baseline inventory and mismatch report

- **Owner:** Maintainer
- **Priority:** P1
- **Target Date:** 2026-06-01
- **Risk:** Low
- **Depends On:** None

**Checklist**
- [x] Inspect `skills/meta-skills/skill-check/assets/skill-check-report-template.html`
- [x] Inspect current skill-check schema section in `report-schema.json`
- [x] Inspect at least one emitted skill-check report sample
- [x] Record mismatch matrix to `docs/reports/adr-0004-contract-baseline.md`

**Acceptance**
- [x] Baseline report lists each mismatch with priority and remediation target

**Completion Note (2026-05-30)**
- Baseline report created: `docs/reports/adr-0004-contract-baseline.md`
- Primary mismatches identified in schema strictness:
  - `spec.checks[].detail` not required
  - `best_practices.warnings` not required
  - `fixes[]` item keys not required

---

### Task 2 — Schema alignment for skill-check contract

- **Owner:** Maintainer
- **Priority:** P1
- **Target Date:** 2026-06-01
- **Risk:** Medium
- **Depends On:** Task 1

**Checklist**
- [x] Update `skills/meta-skills/skill-refine/assets/report-schema.json` skill-check definition as needed
- [x] Ensure required top-level fields match ADR-0004 contract
- [x] Ensure `spec` and `best_practices` required keys are enforced
- [x] Keep `structure.score` string support as legacy compatibility path

**Acceptance**
- [x] Canonical sample validates
- [x] Legacy-compatible `structure.score` string sample validates

**Completion Note (2026-05-30)**
- Tightened skill-check schema requirements in `report-schema.json`:
  - `spec.checks[]` now requires `detail`
  - `best_practices` now requires `warnings`
  - each `fixes[]` item now requires `priority` and `description`
- Preserved legacy compatibility for `structure.score` string path.
- Added regression tests for all newly enforced keys.

---

### Task 3 — Parser and regression tests

- **Owner:** Maintainer
- **Priority:** P1
- **Target Date:** 2026-06-02
- **Risk:** Medium
- **Depends On:** Task 2

**Checklist**
- [x] Extend `test_parse_report.py` with skill-check canonical sample validation path
- [x] Add test for legacy `structure.score` string acceptance
- [x] Add negative test for missing required skill-check top-level fields
- [x] Ensure machine-block-first extraction still selects correct JSON summary

**Acceptance**
- [x] Focused parser/schema tests pass
- [x] Full meta-skill regression suite passes

**Completion Note (2026-05-30)**
- Parser behavior updated for ADR-0004 policy:
  - skill-check reports are machine-block strict (`details#machine-report` required)
  - legacy fallback remains available for other report types (e.g., skill-eval)
- Added regression tests for:
  - reject skill-check fallback extraction (no machine block)
  - accept skill-check machine-block extraction
  - reject missing required skill-check top-level fields
  - schema strictness and legacy compatibility coverage

---

### Task 4 — Documentation/ADR alignment

- **Owner:** Maintainer
- **Priority:** P2
- **Target Date:** 2026-06-02
- **Risk:** Low
- **Depends On:** Task 2

**Checklist**
- [x] Add source-of-truth section to ADR-0004 (schema/template/tests)
- [x] Update implementation notes in ADR-0004 if contract details changed
- [ ] Mark ADR-0004 status transition when implementation is complete

**Acceptance**
- [x] ADR reflects implemented contract and compatibility behavior

**Completion Note (2026-05-30)**
- ADR-0004 updated with explicit machine-block strictness for `skill-check` parsing.
- Compatibility behavior clarified: fallback remains for non-`skill-check` report types only.
- Completion note added summarizing Tasks 1-3 implemented contract details.

---

### Task 5 — Verification and evidence pack

- **Owner:** Maintainer
- **Priority:** P1
- **Target Date:** 2026-06-02
- **Risk:** Low
- **Depends On:** Tasks 1–4

**Checklist**
- [x] Run focused parse-report tests
- [x] Run full meta-skill regression suite
- [x] Validate canonical + legacy sample skill-check payloads against schema
- [x] Produce `docs/reports/adr-0004-pr-evidence.md`

**Acceptance**
- [x] Evidence report created and linked in PR

**Completion Note (2026-05-30)**
- Evidence report created: `docs/reports/adr-0004-pr-evidence.md`
- Focused parser tests and full meta-skill regression suites passed.
- Canonical and legacy skill-check payload samples validated successfully against schema.

## Suggested Command Plan

1. Focused tests:
   - `python3 -m unittest discover -s "skills/meta-skills/skill-refine/scripts/tests" -p "test_parse_report.py"`
2. Full meta-skill regression:
   - four-suite unittest command used by CI
3. Schema sanity checks:
   - validate canonical + legacy skill-check sample payloads against `report-schema.json`

## Risks and Mitigations

### Risk A: Over-tightening breaks legacy reports
- **Mitigation:** retain explicit legacy tolerance for `structure.score` string path

### Risk B: Drift between template and schema
- **Mitigation:** baseline mismatch report + regression tests tied to emitted examples

### Risk C: Parser accidentally picks non-machine `<pre>`
- **Mitigation:** machine-block-first extraction tests for skill-check cases

## Review Checklist (Before Start)

- [ ] Agreement on required skill-check top-level keys
- [ ] Agreement on legacy tolerance scope (`structure.score` only)
- [ ] Agreement on promotion criteria from Proposed -> Accepted

## Approval

- **Plan Approved By:** ____________________
- **Approval Date:** ____________________
