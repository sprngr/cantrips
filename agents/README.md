# Agents

Routing and specialized agents for this repo.

## Files

- `rubber-duck.agent.md`: front-door router for rubber-duck workflows.
- `skill-wizard.agent.md`: planning agent for skill creation.
- `visual-reference.agent.md`: standalone visual research agent.

## Agent to skill-group map

| Agent file | Routes to skills | Skill group | Output shape |
| --- | --- | --- | --- |
| `rubber-duck.agent.md` | `duck-debug`, `duck-design`, `duck-teach`, `duck-triage`, `duck-review` | `skills/rubber-duck/` | Routed duck response based on prompt intent |
| `skill-wizard.agent.md` | `skill-plan` in-session, then handoff to `/skill-forge` | `skills/meta-skills/` | `.skill-plan.yaml` plan artifact |
| `visual-reference.agent.md` | none (no local skill binding) | none | Curated visual references, optional downloaded assets |

## Routing quick reference

- Rubber-duck prompts (`debug`, `design`, `teach`, `what to test`, `review`) -> `rubber-duck.agent.md`.
- Skill authoring planning (`/skill-plan`, refine plan intent) -> `skill-wizard.agent.md`.
- Visual inspiration/reference searches -> `visual-reference.agent.md`.

## Notes

- Source of truth for agent behavior is each `*.agent.md` file in this directory.
- Skill source of truth is under `skills/`.
