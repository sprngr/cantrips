# ADR-0002: `.skill-plan.yaml` Schema Contract

- **Status:** Accepted
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
   - must start with `skills/`
   - must end with `/`
   - absolute paths forbidden (no leading `/`)
   - parent traversal forbidden (no `..` segments)

1a. **Experimental path convention**
   - experimental skills should live under `skills/experimental/<skill-name>/`
   - strict path validity still follows `skills/.../` contract
   - non-experimental placement for experimental skills is allowed but should emit audit warning

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

### Read/Write Compatibility Policy

- **Read contract (migration-safe):** permissive
  - legacy `workflow_notes` object/list/string accepted
  - legacy enum-adjacent strings accepted for migration normalization
- **Write contract (canonical):** strict
  - only canonical enum values written
  - `workflow_notes` written as list of strings only
  - canonical path rule always enforced on write

### Migration Policy (Deterministic)

1. **`target_path` rewrite**
   - strip known workspace prefixes
   - normalize to `skills/.../`
   - enforce trailing slash

2. **`context_assets` rewrite**
   - if already canonical enum, keep
   - if list/composite string (`+`, `,`, whitespace), tokenize left-to-right
   - choose first recognized enum token from source order
   - if no token recognized, set `none` and flag in audit output

3. **`workflow_notes` rewrite**
   - if object, flatten depth-first into bullet strings (`<path>: <value>`)
   - if scalar, wrap as single-item string list
   - preserve semantic content; do not discard non-empty notes

### Enforcement Strategy

- Keep `skills/meta-skills/skill-refine/scripts/validate-plan.sh` backward-compatible for operational use.
- Add strict CI gate script (`scripts/audit-skill-plans.py`) enforcing canonical write contract.
- Migration sequence:
  1. Audit + normalize all tracked plans
  2. Merge migration PR
  3. Enable strict CI enforcement

### Source of Truth

- Contract template: `skills/meta-skills/skill-plan/assets/plan-template.yaml`
- Forge compatibility shape: `skills/meta-skills/skill-forge/assets/plan-template.yaml`
- Runtime validator: `skills/meta-skills/skill-refine/scripts/validate-plan.sh`
- Implementation plan: `docs/adr/0002-implementation-plan.md`

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
- Every tracked `.skill-plan.yaml` passes strict audit gate
- `grep` check confirms no absolute `target_path`
- no non-enum values for constrained fields

## Completion Note (2026-05-30)

- ADR-0002 implementation tasks completed (Task 1-5).
- Strict audit gate added: `scripts/audit-skill-plans.py`.
- Migration completed: baseline violations reduced from 15 -> 0.
- Experimental placement convention established (`skills/experimental/<skill>/`) and documented.
