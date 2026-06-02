# Experimental Skills

Incubation area for skills under active iteration.

## Stability

Experimental skills have **no stability guarantees**.

Expect:
- path/layout changes
- trigger/behavior adjustments
- schema/report contract updates during refinement

Do not treat this directory as long-term stable interface.

## Usage expectations

- Use for evaluation, prototyping, and feedback loops.
- Validate behavior with `skill-check` / `skill-eval` before promoting.
- Keep `.skill-plan.yaml` and report artifacts updated when behavior changes.

## Promotion (experimental -> stable)

Promote a skill out of `experimental/` when all are true:

1. Contract and behavior have stabilized across at least one full refine cycle.
2. `evals/evals.json` exists and quality signal is strong.
3. `skill-check` and `skill-eval` evidence reports show no blocking issues.
4. Paths/docs/triggers are finalized and reflected in root `README.md`.

## Directory policy

All incubating skills should live under:

`src/skills/experimental/<skill>/`

Do not place experimental skills at top-level `src/skills/<skill>/`.

Experimental skill directories are not promoted to `skills/experimental/<skill>/`.
