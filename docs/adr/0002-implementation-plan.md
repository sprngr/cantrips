# ADR-0002 Implementation Plan: `.skill-plan.yaml` Schema Contract

- **Status:** Draft
- **Date:** 2026-05-30
- **Owner:** Repository maintainers
- **Parent ADR:** [ADR-0002](./0002-skill-plan-schema-contract.md)
- **Execution PR:** PR2 (from ADR-0001 delivery strategy)

## Objective

Execute ADR-0002 by normalizing all tracked `.skill-plan.yaml` files to canonical write contract and introducing strict audit enforcement suitable for CI.

## Scope

### In Scope
- Inventory and classify schema drift across tracked `.skill-plan.yaml`
- Add strict audit script for canonical contract
- Migrate all non-conforming `.skill-plan.yaml` artifacts
- Add validation commands and migration verification checklist

### Out of Scope
- Full CI workflow creation (Issue #1 / PR1)
- Eval suite creation (Issue #3)
- Parser hardening (Issue #4)

## Definition of Done (Execution)

- [ ] All tracked `.skill-plan.yaml` pass legacy validator:
      `skills/meta-skills/skill-refine/scripts/validate-plan.sh`
- [ ] All tracked `.skill-plan.yaml` pass strict audit script
- [ ] No `target_path` values are absolute
- [ ] Every `target_path` starts with `skills/` and ends with `/`
- [ ] `context_assets` values are canonical enums only
- [ ] `workflow_notes` serialized as list of strings only
- [ ] Migration report artifact produced and committed (or attached to PR)

## Work Breakdown (Task-Level)

### Task 1 — Baseline inventory and violation report

- **Owner:** Maintainer
- **Priority:** P1
- **Target Date:** 2026-05-31
- **Risk:** Low
- **Depends On:** None

**Checklist**
- [ ] Enumerate all tracked `.skill-plan.yaml` files
- [ ] Capture current values for: `target_path`, `context_assets`, `workflow_notes` type
- [ ] Classify violations by rule category
- [ ] Save report to `docs/reports/skill-plan-audit-baseline.md` (or JSON equivalent)

**Acceptance**
- [ ] Report lists each non-conforming file and exact violation(s)

---

### Task 2 — Add strict audit script (`scripts/audit-skill-plans.py`)

- **Owner:** Maintainer
- **Priority:** P1
- **Target Date:** 2026-06-01
- **Risk:** Medium
- **Depends On:** Task 1

**Checklist**
- [ ] Create script at repo root: `scripts/audit-skill-plans.py`
- [ ] Validate all ADR-0002 strict rules:
  - [ ] `target_path` no leading `/`
  - [ ] `target_path` starts `skills/`
  - [ ] `target_path` ends `/`
  - [ ] `target_path` contains no `..`
  - [ ] enum-only constrained fields
  - [ ] `workflow_notes` list-of-strings
  - [ ] coverage booleans/shape where present
- [ ] Exit non-zero on violation
- [ ] Output machine-readable JSON summary + human-readable text mode
- [ ] Add usage docs header in script

**Acceptance**
- [ ] Script fails on intentionally malformed fixture
- [ ] Script passes against canonical fixture

---

### Task 3 — Deterministic migration of `.skill-plan.yaml`

- **Owner:** Maintainer
- **Priority:** P1
- **Target Date:** 2026-06-02
- **Risk:** Medium
- **Depends On:** Task 2

**Checklist**
- [ ] Normalize `target_path` to `skills/.../`
- [ ] Convert non-enum `context_assets` using ADR-0002 deterministic token rule
- [ ] Flatten `workflow_notes` objects/scalars to list-of-strings
- [ ] Preserve semantic intent notes during flattening
- [ ] Keep diffs minimal beyond required normalization

**Acceptance**
- [ ] All migrated files pass strict audit script
- [ ] No semantic note loss observed in manual spot-check

---

### Task 4 — Backward compatibility and validator alignment

- **Owner:** Maintainer
- **Priority:** P2
- **Target Date:** 2026-06-02
- **Risk:** Medium
- **Depends On:** Task 3

**Checklist**
- [ ] Confirm `validate-plan.sh` remains backward-compatible (read permissive)
- [ ] Confirm strictness enforced by new audit script (write strict)
- [ ] Document dual-gate intent in script comments or docs

**Acceptance**
- [ ] Both validators run successfully on migrated corpus

**Completion Note (2026-05-30)**
- Added dual-gate intent comment block to:
  - `skills/meta-skills/skill-refine/scripts/validate-plan.sh`
- Confirmed validator split in operation:
  - operational/read-permissive: `validate-plan.sh`
  - strict write-contract: `scripts/audit-skill-plans.py`

---

### Task 5 — Verification, reporting, and PR artifacts

- **Owner:** Maintainer
- **Priority:** P1
- **Target Date:** 2026-06-02
- **Risk:** Low
- **Depends On:** Tasks 1–4

**Checklist**
- [ ] Run legacy validator across all plans
- [ ] Run strict audit script across all plans
- [ ] Regenerate final migration report:
      `docs/reports/skill-plan-audit-after.md`
- [ ] Include before/after counts by violation type
- [ ] Prepare PR checklist and evidence snippets

**Acceptance**
- [ ] PR includes commands + outputs proving contract compliance

## Suggested Command Plan (Execution)

> Adjust command paths if scripts move during implementation.

1. Baseline list:
   - `python3 scripts/audit-skill-plans.py --format markdown > docs/reports/skill-plan-audit-baseline.md`
2. Legacy validator pass:
   - loop all `.skill-plan.yaml` through `skills/meta-skills/skill-refine/scripts/validate-plan.sh`
3. Strict audit pass:
   - `python3 scripts/audit-skill-plans.py --fail-on-violation`
4. Post-migration report:
   - `python3 scripts/audit-skill-plans.py --format markdown > docs/reports/skill-plan-audit-after.md`

## Risks and Mitigations

### Risk A: ambiguous `context_assets` composite strings
- **Impact:** inconsistent normalization
- **Mitigation:** deterministic left-to-right token selection + audit warning

### Risk B: loss of nuance when flattening `workflow_notes`
- **Impact:** degraded planning context
- **Mitigation:** path-prefixed flattening (`pipeline.step: ...`), manual spot-check on complex plans

### Risk C: future drift after migration
- **Impact:** regression to non-canonical artifacts
- **Mitigation:** strict audit script integrated into CI gate (Issue #1 follow-through)

## Review Checklist (Before Start)

- [ ] Team agrees on deterministic rewrite policy
- [ ] Team agrees on strict-vs-permissive validator split
- [ ] Team agrees on report artifact location (`docs/reports/`)
- [ ] Team agrees this plan ships in PR2 scope

## Approval

- **Plan Approved By:** ____________________
- **Approval Date:** ____________________
