# Meta-Skills

Toolkit for agent-skill development lifecycle.

Each component has a single responsibility.
`.skill-plan.yaml` is the canonical artifact across the whole loop.

## Planning agent

- `agents/skill-wizard.agent.md` starts the workflow and runs the planning interview.
- Planning phase ends when an approved `.skill-plan.yaml` is written.
- After planning, run forge/check/eval/refine from your normal agent workflow.

## Toolkit

| Component | Responsibility | Input | Output |
| --- | --- | --- | --- |
| `skill-wizard` (agent) | Tiered interview orchestrator for planning stage | User intent | Approved plan workflow |
| `skill-plan` | Decision capture and schema-complete plan authoring | Interview answers | `.skill-plan.yaml` |
| `skill-forge` | Generate and validate bundle from plan | `.skill-plan.yaml` | Skill bundle (`SKILL.md`, `scripts/`, `references/`) |
| `skill-check` | Spec and best-practice audit | Skill bundle | `*-skill-check-report.html` |
| `skill-eval` | Test and benchmark behavior | Skill bundle | Eval workspace + `eval-report.html` |
| `skill-refine` | Patch plan from audit/eval feedback | Reports + user guidance | `.skill-plan.patch.yaml`, `.skill-plan.patched.yaml` |

## Workflow

Human in loop at every stage. No automatic orchestration.

```text
       [ User Intent ]
              |
              v
   [ skill-wizard + skill-plan ] -- (tiered planning)
              |
              v
      +------------------+
      | .skill-plan.yaml |
      +---------+--------+
                |
                v
        [   skill-forge   ] -- (generate + validate)
                |
                v
         +--------------+
         | Skill Bundle |
         +------+-------+
                |
        +-------+-------+
        |               |
        v               v
 [  skill-check ]   [  skill-eval  ]
        |               |
        v               v
 +-------------+   +-------------+
 | check-report|   |  eval-logs  |
 +------+------+   +------+------+
        |               |
        +-------+-------+
                |
                v
        [  skill-refine  ] -- (patch plan)
                |
                +------------------------------+
                                               |
                                               v
                                  +---------------------------+
                                  | .skill-plan.patched.yaml |
                                  +-------------+-------------+
                                                |
                                                v
                                         [ skill-forge ]
                                                |
                                                v
                               repeat check/eval/refine loop
```

## Example tracer-bullet flow

Scenario: build `pr-risk-triage` skill.

### 1) Plan

Prompt to `skill-wizard`:

```text
Build a PR risk triage skill. Use scripts for deterministic scoring and AI for rationale.
```

Expected artifact:

```text
src/skills/pr-risk-triage/.skill-plan.yaml
```

### 2) Forge from plan

```text
/skill-forge src/skills/pr-risk-triage/.skill-plan.yaml
```

Expected bundle:

```text
src/skills/pr-risk-triage/
  SKILL.md
  scripts/
  references/
```

Promoted install artifact path after build:

```text
skills/pr-risk-triage/
```

### 3) Run audit and eval

```text
/skill-check src/skills/pr-risk-triage
/skill-eval src/skills/pr-risk-triage
```

Expected feedback artifacts:

```text
*-skill-check-report.html
eval-report.html
```

### 4) Patch plan from feedback

```text
/skill-refine src/skills/pr-risk-triage/.skill-plan.yaml
```

Expected outputs:

```text
src/skills/pr-risk-triage/.skill-plan.patch.yaml
src/skills/pr-risk-triage/.skill-plan.patched.yaml
```

### 5) Re-forge from patched plan

```text
/skill-forge src/skills/pr-risk-triage/.skill-plan.patched.yaml
```

Repeat forge/check/eval/refine loop until quality target is met.

## Pass criteria checklist

- [ ] `skill-wizard` writes valid `.skill-plan.yaml` with `completed: true` after approval.
- [ ] `skill-forge` imports plan without schema or enum errors.
- [ ] Generated bundle contains expected tier artifacts (`SKILL.md`, `scripts/`, `references/`).
- [ ] `skill-check` report has no blocking spec violations (or fewer than previous round).
- [ ] `skill-eval` shows measurable improvement vs baseline (pass rate/readiness).
- [ ] `skill-refine` writes both `.skill-plan.patch.yaml` and `.skill-plan.patched.yaml`.
- [ ] Re-forge from patched plan succeeds without manual interview fallback.
- [ ] Second check/eval round improves or confirms target quality.
