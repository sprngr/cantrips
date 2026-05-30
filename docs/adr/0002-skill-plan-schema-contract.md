# ADR-0002: `.skill-plan.yaml` Schema Contract

- **Status:** Proposed
- **Date:** 2026-05-30
- **Deciders:** Repository maintainers
- **Related:** ADR-0001, SDLC Issue #2

## Context

Planning artifacts currently show drift across skills:
- absolute and relative `target_path` mixed
- enum fields represented as free-form strings in some plans
- shape inconsistency between planning-stage and completed plans

This creates fragile interop between `skill-wizard`, `skill-plan`, `skill-forge`, and `skill-refine`.

## Decision

Adopt a single canonical contract for `.skill-plan.yaml` with strict field rules and state semantics.

### Contract Rules

1. **Path rule**
   - `target_path` must be workspace-relative
   - must end with `/`
   - absolute paths forbidden

2. **Enum rule**
   - `scope ∈ {single, moderate, extended}`
   - `mechanism ∈ {reasoning, scripts, hybrid}`
   - `context_assets ∈ {none, schema, templates, checklists, manuals}`
   - `tier ∈ {A, B, C}`
   - `example_placed ∈ {inline, references/Example.md}`

3. **Lifecycle rule**
   - planning state: `completed: false`
   - forge input state: `completed: true`
   - `example_generated` flips true only after example generation step

4. **Coverage rule**
   - `coverage.essential_schema` keys must all exist
   - keys are boolean only
   - `unanswered_branches` must be array

5. **Workflow notes rule**
   - must be list of strings in canonical saved artifact
   - if richer internal structure used during interview, it must be normalized before final write

### Source of Truth

- Contract template: `skills/meta-skills/skill-plan/assets/plan-template.yaml`
- Forge compatibility shape: `skills/meta-skills/skill-forge/assets/plan-template.yaml`
- Runtime validator: `skills/meta-skills/skill-refine/scripts/validate-plan.sh`

## Consequences

### Positive
- Portable plans across machines and environments
- Predictable imports for forge/refine
- Simpler CI validation

### Negative
- Legacy plans require migration
- Slightly stricter authoring constraints

## Implementation Notes

1. Create schema/audit script to assert all above rules.
2. Normalize existing plans in one migration PR.
3. Add CI gate to fail non-conforming plans.
4. Update skill docs to reference canonical contract explicitly.

## Verification

- Every tracked `.skill-plan.yaml` passes validator
- `grep` check confirms no absolute `target_path`
- no non-enum values for constrained fields
