# ADR-0003 Implementation Plan: `skill-eval` JSON Summary Contract

- **Status:** Draft
- **Date:** 2026-05-30
- **Owner:** Repository maintainers
- **Parent ADR:** [ADR-0003](./0003-skill-eval-json-summary-contract.md)
- **Execution PR:** Next ADR execution PR after ADR-0002

## Objective

Stabilize `skill-eval` machine-readable JSON summary contract and ensure report output, schema validation, parser compatibility, and tests all align to one canonical payload.

## Scope

### In Scope
- Align `skill-eval` report JSON summary shape to ADR-0003 canonical contract
- Synchronize `skill-refine` report schema with ADR-0003 fields
- Add contract tests for positive and negative examples
- Ensure parser compatibility with machine-block extraction

### Out of Scope
- `skill-check` JSON contract changes (ADR-0004)
- full roll-up dashboard implementation (separate issue)

## Definition of Done (Execution)

- [ ] Canonical required fields emitted in `skill-eval` JSON summary
- [ ] `iteration` normalized to string `iteration-N`
- [ ] metric objects use `{pass_rate,stddev,samples,tokens,time}` consistently
- [ ] `skills/meta-skills/skill-refine/assets/report-schema.json` updated and valid
- [ ] parser tests cover canonical and drift cases
- [ ] no `time_seconds`/`time` contract ambiguity remains

## Work Breakdown (Task-Level)

### Task 1 — Contract inventory and mismatch report

- **Owner:** Maintainer
- **Priority:** P1
- **Target Date:** 2026-06-01
- **Risk:** Low
- **Depends On:** None

**Checklist**
- [x] Inspect current `skill-eval` report template + emitted JSON samples
- [x] Inspect `report-schema.json` eval definition
- [x] Record mismatches vs ADR-0003 required/recommended fields
- [x] Write short inventory note to `docs/reports/adr-0003-contract-baseline.md`

**Completion Note (2026-05-30)**
- Baseline report created: `docs/reports/adr-0003-contract-baseline.md`
- Single mismatch identified: schema currently permits integer `iteration`; ADR-0003 canonical contract prefers `iteration-N` string only.

---

### Task 2 — Align schema and output contract

- **Owner:** Maintainer
- **Priority:** P1
- **Target Date:** 2026-06-01
- **Risk:** Medium
- **Depends On:** Task 1

**Checklist**
- [x] Update `skills/meta-skills/skill-refine/assets/report-schema.json` for ADR-0003 canonical shape
- [x] Ensure `iteration` is string pattern `iteration-N` in contract examples
- [x] Ensure metric subobject keys use `time` (seconds) consistently
- [x] Preserve additive compatibility where feasible

**Acceptance**
- [x] Schema validates canonical payload examples

**Completion Note (2026-05-30)**
- Updated `skill-eval-report.iteration` to strict string pattern `^iteration-[0-9]+$`.
- Required metric keys now enforced on both `with_skill` and `without_skill`:
  `pass_rate`, `stddev`, `samples`, `tokens`, `time`.
- Added regression tests:
  - reject integer `iteration`
  - reject missing required metric key(s)

---

### Task 3 — Strengthen parser and contract tests

- **Owner:** Maintainer
- **Priority:** P1
- **Target Date:** 2026-06-02
- **Risk:** Medium
- **Depends On:** Task 2

**Checklist**
- [x] Extend `skills/meta-skills/skill-refine/scripts/tests/test_parse_report.py`
- [x] Add positive tests for canonical eval payload
- [x] Add negative tests for missing required fields / wrong type
- [x] Add mixed-template test to ensure machine-block extraction remains robust

**Acceptance**
- [x] Test suite passes with updated contract

**Completion Note (2026-05-30)**
- Parser hardening implemented in `parse_report.py`:
  - machine-block-first extraction (`details#machine-report > pre`)
  - legacy fallback to first parseable `<pre>` JSON
  - output now includes `extraction_mode` (`machine`, `fallback`, `none`)
- Added parser tests for:
  - machine block preference over unrelated `<pre>`
  - fallback behavior when machine block is absent
  - `main()` output includes `extraction_mode`
  - existing schema strictness tests remain green

---

### Task 4 — Documentation alignment

- **Owner:** Maintainer
- **Priority:** P2
- **Target Date:** 2026-06-02
- **Risk:** Low
- **Depends On:** Task 2

**Checklist**
- [x] Update `skills/meta-skills/skill-eval/SKILL.md` JSON schema example (if drift exists)
- [x] Add/verify explicit contract reference note in ADR-0003
- [x] Add completion note when implementation done

**Acceptance**
- [x] Docs and schema examples match implemented payload

**Completion Note (2026-05-30)**
- Added explicit iteration contract rule in `skills/meta-skills/skill-eval/SKILL.md`:
  `iteration` must be string `iteration-N`.
- Updated ADR-0003 status to Accepted.
- Added ADR-0003 "Contract Source of Truth" section linking schema, template, and parser tests.

---

### Task 5 — Verification + evidence pack

- **Owner:** Maintainer
- **Priority:** P1
- **Target Date:** 2026-06-02
- **Risk:** Low
- **Depends On:** Tasks 1–4

**Checklist**
- [x] Run parse-report test suite
- [x] Run full meta-skill tests for regression confidence
- [x] Validate sample eval summary against schema
- [x] Produce `docs/reports/adr-0003-pr-evidence.md` with command list + outcomes

**Acceptance**
- [x] Evidence report created and linked in PR

**Completion Note (2026-05-30)**
- Evidence report created: `docs/reports/adr-0003-pr-evidence.md`
- Focused parser tests and full meta-skill regression suites passed.
- Canonical sample validated successfully against updated schema.

## Suggested Command Plan

1. Run focused parser tests:
   - `python3 -m unittest discover -s "skills/meta-skills/skill-refine/scripts/tests" -p "test_parse_report.py"`
2. Run full meta-skill suite:
   - existing four-suite unittest command used in CI
3. Optional schema sanity run:
   - lightweight Python check loading `report-schema.json` and validating canonical sample

## Risks and Mitigations

### Risk A: Breaking downstream parse on field rename
- **Mitigation:** keep compatibility in parser, tighten schema with clear migration notes

### Risk B: Hidden drift between template and schema
- **Mitigation:** add explicit contract tests using real template-style payloads

### Risk C: Time unit confusion (`time` vs `time_seconds`)
- **Mitigation:** lock on `time` seconds in ADR + schema + tests

## Review Checklist (Before Start)

- [ ] Agreement on canonical required fields
- [ ] Agreement on `iteration-N` string convention
- [ ] Agreement on additive-only compatibility policy

## Approval

- **Plan Approved By:** ____________________
- **Approval Date:** ____________________
