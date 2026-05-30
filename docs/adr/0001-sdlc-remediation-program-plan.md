# ADR-0001: SDLC Remediation Program Plan

- **Status:** Accepted
- **Date:** 2026-05-30
- **Deciders:** Repository maintainers
- **Context:** `SDLC_AUDIT_REPORT.html`, `SDLC_ACTIONABLE_ISSUES.md`

## Context

SDLC audit identified nine actionable issues across CI, schema hygiene, evaluation coverage, parser resilience, process docs, portfolio observability, and governance.

Current deficits:
- No CI quality gate
- Inconsistent `.skill-plan.yaml` contract adherence
- Sparse eval coverage for skill portfolio
- Parser fragility risk in `skill-refine`
- Missing contributor/testing process docs
- Missing roll-up quality reporting
- Missing ADR governance baseline

Need one execution plan tying all issues into staged, low-risk delivery.

## Decision

Adopt a phased remediation program with explicit dependency ordering, per-issue Definition of Done, and measurable exit criteria.

### Phase Plan

1. **Foundation Gates (P1 first):** Issues #1, #2
2. **Coverage Expansion:** Issue #3
3. **Meta-skill Hardening:** Issues #4, #6
4. **Operational Documentation & Visibility:** Issues #5, #7
5. **Long-tail Resilience:** Issues #8, #9

## Issue-by-Issue Planning Breakdown

---

### Issue #1 — [P1] Add CI quality gate for skills/meta-skills

**Objective**
Create mandatory automated quality gate for tests and structural checks.

**Dependencies**
- None (start here)

**Work Plan**
1. Create `.github/workflows/skills-quality.yml`
2. Add steps:
   - Run meta-skill script unit tests
   - Run structure validation across all `skills/**/SKILL.md`
   - Run eval-presence policy script for required skills
3. Fail workflow on any gate violation
4. Document local parity command in `TESTING.md`

**Definition of Done**
- CI runs on push/PR
- Red builds for failing tests/validation/policy
- Green baseline on current main after remediation changes

**Risks**
- False positives due to current plan/eval drift

**Mitigation**
- Land with temporary allowlist only if strictly needed; remove in next PR

---

### Issue #2 — [P1] Normalize `.skill-plan.yaml` artifacts

**Objective**
Enforce canonical planning artifact shape for portability and forge/refine compatibility.

**Dependencies**
- Can start in parallel with Issue #1, but must finish before strict CI enforcement

**Work Plan**
1. Enumerate all `.skill-plan.yaml`
2. Validate against canonical rules (enum/path/completed/state fields)
3. Patch non-conforming files
4. Add audit script (`scripts/audit-skill-plans.py` or equivalent)
5. Integrate audit into CI gate

**Definition of Done**
- No absolute `target_path`
- No non-enum `context_assets`
- All plans pass `skills/meta-skills/skill-refine/scripts/validate-plan.sh`

**Risks**
- Historical plan intent may be lost during normalization

**Mitigation**
- Keep changes minimal; include rationale comments where needed

---

### Issue #3 — [P1] Add baseline eval suites for missing skills

**Objective**
Establish minimum behavior benchmark across entire skill portfolio.

**Dependencies**
- Issue #1 CI scaffold available
- Prefer Issue #2 complete first for clean contracts

**Work Plan**
1. Create `evals/evals.json` for 9 missing skills
2. Include at least 3 tests each (normal / edge / malformed)
3. Validate schema compatibility with `skill-eval/assets/evals-schema.json`
4. Add CI policy ensuring presence for required skills

**Definition of Done**
- 12/12 skills have baseline eval definitions
- All eval files schema-valid

**Risks**
- Low-signal assertions may create fake confidence

**Mitigation**
- Mark baseline as smoke-level; schedule iterative hardening

---

### Issue #4 — [P1] Harden `skill-refine` parser against template drift

**Objective**
Make report parsing robust to HTML template evolution.

**Dependencies**
- None hard; can run in parallel with #3

**Work Plan**
1. Refactor parser to locate machine-summary JSON deterministically
2. Add fallback extraction strategies
3. Return explicit actionable error outputs
4. Add multi-`<pre>` and malformed-structure tests

**Definition of Done**
- Parser passes new drift tests
- Existing tests remain green

**Risks**
- Overfitting parser to current template variants

**Mitigation**
- Prefer semantic anchor strategy (id/summary markers), not positional selection

---

### Issue #5 — [P2] Add contributor/process docs

**Objective**
Codify contributor workflow and quality expectations.

**Dependencies**
- CI commands from #1 should be stable

**Work Plan**
1. Add `CONTRIBUTING.md`
2. Add `TESTING.md`
3. Define DoD for skill changes (plan/check/eval expectations)
4. Link docs from root README

**Definition of Done**
- New contributors can run full verification from docs only

---

### Issue #6 — [P2] Add self-eval pipeline for meta-skills

**Objective**
Evaluate quality tools with same rigor they enforce.

**Dependencies**
- Issue #3 eval framework availability

**Work Plan**
1. Add eval definitions for `skill-check`, `skill-eval`, `skill-refine`
2. Run iteration-1 eval cycle for each
3. Capture reports and findings
4. Create follow-up issues for observed defects

**Definition of Done**
- All three meta-skills produce at least one eval report

---

### Issue #7 — [P2] Add quality status roll-up artifact

**Objective**
Provide portfolio-wide visibility into readiness.

**Dependencies**
- CI and eval presence work from #1/#3

**Work Plan**
1. Add report-generation script (`docs/reports/` output)
2. Include: plan conformance, eval presence, latest check/eval artifacts
3. Wire into CI and README

**Definition of Done**
- Single generated status artifact includes all skills

---

### Issue #8 — [P3] Add `squash` script unit tests

**Objective**
Close remaining test gap in high-utility skill scripts.

**Dependencies**
- CI pipeline from #1

**Work Plan**
1. Add test harness under `skills/squash/scripts/tests/`
2. Cover happy path + 2+ failure cases
3. Ensure deterministic temp-file handling

**Definition of Done**
- Tests integrated and green in CI

---

### Issue #9 — [P3] Introduce ADR governance baseline

**Objective**
Capture contract decisions and reduce future drift.

**Dependencies**
- None; starts now via this ADR

**Work Plan**
1. Keep `docs/adr/` index updated
2. Add ADRs for:
   - plan schema contract
   - eval summary JSON contract
   - skill-check report JSON contract
3. Link ADR index in README

**Definition of Done**
- ADR directory active with at least 3 follow-up contract ADRs

**Progress Note (2026-05-30)**
- Completed: `docs/adr/` index created
- Completed: ADR-0002 (`.skill-plan.yaml` schema contract)
- Completed: ADR-0003 (`skill-eval` JSON summary contract)
- Completed: ADR-0004 (`skill-check` JSON summary contract)

---

## Delivery Strategy

Use incremental PRs, one issue per PR (except tightly coupled items):
- PR1: #1 + minimal scaffolding for #9
- PR2: #2
- PR3: #3
- PR4: #4
- PR5: #5 + #7
- PR6: #6
- PR7: #8
- PR8: optional follow-on governance refinements (if new contract ADRs emerge)

## Success Metrics

- 100% skills with `evals/evals.json`
- 100% `.skill-plan.yaml` pass contract validation
- CI required and passing on main
- Portfolio roll-up report generated per CI run
- ADR log current for core contract changes

## Consequences

### Positive
- Higher confidence in skill behavior
- Faster onboarding and contribution
- Reduced schema/report drift over time

### Negative
- Initial throughput slowdown while gates land
- Additional maintenance overhead for eval and ADR updates

### Neutral/Tradeoff
- More explicit process in exchange for lower long-term rework
