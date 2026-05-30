# Cantrips

🔮 Because I'm still not convinced this isn't magic.

Repository of personal agent skills, helper agents, and skill-authoring playbooks.

> [!NOTE]
> My preferred harness is [OpenCode](https://opencode.ai/) so you may need to make some tweaks.

## What lives here

- `skills/rubber-duck/`: practical rubber-duck skills (`duck-debug`, `duck-design`, `duck-teach`, `duck-triage`, `duck-review`).
- `skills/meta-skills/`: skill-building toolkit (`skill-plan`, `skill-forge`, `skill-check`, `skill-eval`, `skill-refine`) plus docs and helper scripts.
- `agents/`: routing and specialized agents (`🦆`, `skill-wizard`, `visual-reference`).
- `archive/`: historical planning docs; useful context, not active source of truth.

## Agent to skill-group map

| Agent | Owns/Routs to | Skill group | Notes |
| --- | --- | --- | --- |
| `🦆` (`agents/rubber-duck.agent.md`) | `duck-debug`, `duck-design`, `duck-teach`, `duck-triage`, `duck-review` | `skills/rubber-duck/` | Front-door router for rubber-duck workflows; asks 1 clarifying question on unrecognized prompts. |
| `skill-wizard` (`agents/skill-wizard.agent.md`) | `skill-plan` (active in-session), then handoff to `/skill-forge` | `skills/meta-skills/` | Planning-only agent; outputs `.skill-plan.yaml` and does not generate bundle artifacts directly. |
| `visual-reference` (`agents/visual-reference.agent.md`) | (no local skill binding) | none | Standalone specialized agent for visual research and reference curation. |

## Skill index

| Skill | Group | Trigger examples | Primary output |
| --- | --- | --- | --- |
| `duck-debug` | rubber-duck | `debug this`, `why broken` | Root-cause trace + next checks |
| `duck-design` | rubber-duck | `design this`, `tradeoffs` | Architecture options + tradeoff framing |
| `duck-teach` | rubber-duck | `teach me X`, `how does X work` | Structured explanation (what/why/example/pitfalls) |
| `duck-triage` | rubber-duck | `what to test`, `triage this bug` | Test/priority plan + risk coverage |
| `duck-review` | rubber-duck | `review this`, `review diff` | One-line review findings + fixes |
| `skill-plan` | meta-skills | `/skill-plan`; planning stage in `skill-wizard` | Planning rules and schema guidance for `.skill-plan.yaml` |
| `skill-forge` | meta-skills | `/skill-forge <plan-path>` | Generated skill bundle from completed plan |
| `skill-check` | meta-skills | `audit skill`, `skill check` | Spec and best-practice audit HTML report |
| `skill-eval` | meta-skills | `eval skill`, `run evals` | Benchmark/eval workspace + `eval-report.html` |
| `skill-refine` | meta-skills | `refine skill`, `/skill-refine` | `.skill-plan.patch.yaml` + `.skill-plan.patched.yaml` |

## Install

Install full repo skill set from a compatible runtime:

```bash
npx skills add sprngr/cantrips --full-depth
```

Or install from local clone while developing:

```bash
npx skills add /path/to/cantrips --full-depth
```

Install included agents, depends on where your preferred harness stores them (ex: ~/.config/opencode/agents for OpenCode, ~/.copilot/agents for Copilot):

```bash
cp /path/to/cantrips/agents/*.agent.md /path/to/harness/agents/
```

## How to work in this repo

1. Edit skill content in `skills/<group>/<skill>/` (`SKILL.md`, `scripts/`, `references/`, `assets/`).
2. Edit agent routing/behavior in `agents/*.agent.md`.
3. Reinstall from local path (command above) to test changes in your agent runtime.
4. For new skill authoring, use meta-skill flow:
   - `skill-wizard` -> writes `.skill-plan.yaml`
   - `/skill-forge <plan-path>` -> generates skill bundle
   - `/skill-check` and `/skill-eval` -> audit + benchmark
   - `/skill-refine` -> patch plan and iterate

## Conventions

- Keep skills single-purpose; avoid overlapping responsibilities.
- Keep scripts deterministic where possible; keep policy/heuristics in `SKILL.md`.
- Treat `.skill-plan.yaml` as the canonical planning artifact for generated skills.
