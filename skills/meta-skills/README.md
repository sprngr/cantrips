# Meta-Skills

A toolkit for the agent skills development lifecycle.

Each tool has a single responsibility. `.skill-plan.yaml` is the source of truth throughout.

## Toolkit

| Skill | Responsibility | Input | Output |
|---|---|---|---|
| **skill-wizard** (agent) | Interrogation engine (tiered by complexity) | User intent | Triggers skill-plan |
| **skill-plan** | Decision capture | Interview answers | `.skill-plan.yaml` |
| **skill-forge** | Generate + validate from plan | `.skill-plan.yaml` | Skill bundle |
| **skill-check** | Audit against spec | Skill bundle | check-report |
| **skill-eval** | Test & benchmark | Skill bundle | eval-logs |
| **skill-refine** | Patch plan from feedback | Reports / user input | Patched `.skill-plan.yaml` |

## Flow

Human-in-the-loop at every stage. No automated orchestration.

```
       [ User Intent ]
              │
              ▼
      [ skill-wizard ] ──────(Tiered Interrogation)
              │
              ▼
      [  skill-plan  ] ──────(Decision Capture)
              │
              ▼
      ┌──────────────────┐
      │ .skill-plan.yaml │◄────────────────────────────────┐
      └────────┬─────────┘                                 │
               │                                           │ (Patches yaml)
               ▼                                           │
      [  skill-forge  ] ──────(Generate + Validate)        │
               │                                           │
               ▼                                           │
      ┌───────────────┐                                    │
      │  Skill Bundle │                                    │
      └───────┬───────┘                                    │
              │                                            │
              ├────────────────────┐                       │
              ▼                    ▼                       │
      [ skill-check ]      [  skill-eval  ]                │
              │                    │                       │
              ▼                    ▼                       │
      ┌──────────────┐     ┌──────────────┐                │
      │ check-report │     │  eval-logs   │                │
      └──────┬───────┘     └──────┬───────┘                │
             │                    │                        │
             └────────┬───────────┘                        │
                      ▼                                    │
              [ skill-refine ] ────────────────────────────┘
```

## Example working flow (tracer bullet)

Scenario: build `pr-risk-triage` skill.

### 1) Plan the skill

User prompt to skill-wizard:

```text
Build a PR risk triage skill. Use scripts for deterministic scoring and AI for rationale.
```

Expected output artifact:

```text
skills/pr-risk-triage/.skill-plan.yaml
```

### 2) Generate bundle from plan

```text
/skill-forge skills/pr-risk-triage/.skill-plan.yaml
```

Expected bundle:

```text
skills/pr-risk-triage/
  SKILL.md
  scripts/
  references/
```

### 3) Run audits and evals

```text
/skill-check skills/pr-risk-triage
/skill-eval skills/pr-risk-triage
```

Expected feedback artifacts:

```text
*-skill-check-report.html
eval-report.html
```

### 4) Patch plan from feedback

```text
/skill-refine skills/pr-risk-triage/.skill-plan.yaml
```

Expected outputs:

```text
skills/pr-risk-triage/.skill-plan.patch.yaml
skills/pr-risk-triage/.skill-plan.patched.yaml
```

### 5) Re-forge from patched plan

```text
/skill-forge skills/pr-risk-triage/.skill-plan.patched.yaml
```

Repeat check/eval/refine loop until quality target is met.

## Pass criteria checklist

- [ ] `skill-wizard` writes a valid `.skill-plan.yaml` with `completed: true` on approve
- [ ] `skill-forge` imports the plan without schema/enum errors
- [ ] Generated bundle includes expected tier artifacts (`SKILL.md`, `scripts/`, `references/`)
- [ ] `skill-check` produces report with no blocking spec violations (or fewer than previous round)
- [ ] `skill-eval` shows measurable improvement vs baseline (pass rate/readiness)
- [ ] `skill-refine` outputs both `.skill-plan.patch.yaml` and `.skill-plan.patched.yaml`
- [ ] Re-forge from patched plan succeeds without manual interview fallback
- [ ] Second check/eval round improves or confirms target quality
