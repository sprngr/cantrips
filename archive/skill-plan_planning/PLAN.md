# skill-plan

A planning skill that powers skill-wizard's tiered interview (quick for simple skills, deep for complex skills) before `skill-forge` generation.

## Delta

| vs | skill-forge | grill-me |
|--|--|--|
| **Depth** | Generation-only (no interview) | Unbounded, dynamic pattern matching |
| **Domain** | Build/synthesis from plan yaml | agentskills.io schema expert |
| **Routing** | Fixed turns (intent → scope → mechanism → context → path) | Pattern branches against previous answers, 1 follow-up per turn |
| **Validation** | Draft anti-patterns + clarity checklist (post-plan) | Coverage checklist gates (pre-generation) |

## Architecture

```
agent: skill-wizard.agent.md
  - State machine, tiered interview routing, YAML I/O, backtrack
  - Selects quick (3-4 turns) or deep (dynamic) planning mode
  - Handles approve/deny/edit gate
  - Writes `.skill-plan.yaml` on approve
  - Hands off explicitly (no auto-invoke)

skill: skill-plan (in skills/meta-skills/skill-plan/)
  - Pattern matching rules (8-10 main branches)
  - Terminology glossary (agentskills.io term map)
  - Edge case triggers (pattern-index.md)
  - Anti-pattern + schema validation rules

pipeline:
  user "create skill" OR /skill-plan → skill-wizard
  skill-wizard selects interview depth (quick or deep)
  skill-wizard validates + review gate → writes `.skill-plan.yaml`
  user runs skill-forge with plan path → skill-forge imports plan → Blueprint → Draft → Write
```

## Routing Rules

- **skill-wizard is entry point** for planning before generation.
- `/skill-plan` explicitly invokes skill-wizard planning mode.
- skill-wizard chooses interview depth:
  - quick mode for simple intents (single task, low orchestration)
  - deep mode for complex intents (pipeline/orchestration/multi-role/hybrid)
- User may override mode (`quick` or `deep`) explicitly.

## State Machine

### 0. Entry
* Route via `/skill-plan` or skill creation intent.
* Read existing `.skill-plan.yaml` if present. Restore state if `completed: false`.

### 0.5. Interview Depth Selection
* Ask one question when needed: "Use quick planning (3-4 turns) or deep planning (dynamic)?"
* If simple + user agrees quick → enter quick interview path.
* If complex or user requests depth → enter deep interview path.

### 1. Intent + Pattern Match (Loop)
* Ask single follow-up question based on last answer (see Pattern Matching Rules).
* **Guardrail:** Exactly 1 question per turn. Never stack questions.
* Write answer to `turns[]` in `.skill-plan.yaml`.
* Update `coverage.essential_schema` for any field the answer resolves.
* Check coverage checklist. If incomplete → continue loop. If complete → State 2.

### 2. Review Gate
* Show `.skill-plan.yaml` preview (YAML only, no SKILL.md preview).
* Ask: "Approve, Deny, or Edit a field?"
* **Approve** → set `completed: true`, persist YAML, exit to State 3.
* **Deny** → backtrack to nearest fork point, re-enter State 1 from that fork.
* **Edit** → ask which field to refine, adjust, re-check coverage, stay in State 2.

### 3. Handoff
* `.skill-plan.yaml` written to `target_path`.
* Present explicit handoff: "Start skill-forge: `/skill-forge <target_path>/.skill-plan.yaml` or open new session with that path."
* Do NOT auto-invoke skill-forge. User starts fresh session.

## Pattern Matching Rules

* Implemented in SKILL.md (8-10 primary branches).
* Dynamic: next question derived from previous answer, not fixed turn order.
* Edge cases in `references/pattern-index.md`.
* Example: answer implies scripting → next question probes mechanism → if hybrid → next probes context_assets.

## Fork Tracking & Backtrack

* Each State 1 loop that resolves ≥1 coverage field is a fork point.
* `last_backtrack_turn` in YAML tracks the most recent fork turn index.
* On **Deny**: scan `turns[]` from newest to oldest, find nearest turn where ≥2 valid paths existed. Set `last_backtrack_turn` to that index, truncate `turns[]` downstream, re-enter State 1.
* On **Edit**: no fork change. Refine in place, stay at State 2.

## Coverage Tracking Mechanics

* `coverage.essential_schema` mirrors checklist keys. Starts all `false`.
* After each State 1 turn, scan answer for schema-relevant content. Set matched key to `true`.
* `coverage.unanswered_branches` is a list of strings describing pending pattern branches (e.g., "mechanism not yet resolved to reasoning vs hybrid").
* Stop condition: all `essential_schema` true AND `unanswered_branches` is `[]`.
* `name`/`description` not tracked by skill-plan. Left for skill-forge Blueprint phase. `coverage.agentskills_io_mandatory` block exists as a placeholder for skill-forge to populate.

## Coverage Checklist (stop condition)

Delegated to skill-forge (handled during Blueprint phase, not skill-plan):
- name, description (<3 sentences including `Use when` triggers)

Essential (`.skill-plan.yaml`) — tracked via `coverage.essential_schema`:
1. intent statement
2. scope (single | moderate | extended)
3. mechanism (reasoning | scripts | hybrid)
4. context_assets (none | schema | templates | checklists | manuals)
5. tier (A | B | C)
6. target_path (workspace-relative)
7. workflow_notes (list)
8. example_placed (inline | references/Example.md)
9. example_generated (true | false)

**When all 9 slots filled + `coverage.unanswered_branches` empty → stop + review gate.**

## Review Gate

- **Output**: `.skill-plan.yaml` only (no SKILL.md preview — that's skill-forge's Blueprint)
- **Validation**: agentskills.io mandatory field coverage + schema field completeness
- **Gates**: approve (→ write YAML → invite skill-forge import) / deny (→ nearest-fork backtrack) / edit (→ refine specific turn)
- **User-force-exit** always available (e.g., `exit` or "done")

## File Structure (development path)

```
skills/meta-skills/skill-plan/
  SKILL.md                  # Domain knowledge, patterns, glossary, anti-patterns
  assets/
    plan-template.yaml      # Local planning-state template
  references/
    terminology.md          # agentskills.io term map
    pattern-index.md        # Edge case triggers
agents/skill-wizard.agent.md  # State machine, routing, YAML I/O
PLAN.md                     # This file
```

## Development → Install

Built in `skills/meta-skills/skill-plan/`. Installed via `npx skills add <path>`.

## .skill-plan.yaml Schema

Maintained in `skill-plan/assets/plan-template.yaml`. Compatible with skill-forge input contract and extends with coverage tracking:

```yaml
# .skill-plan.yaml - Planning state artifact produced by skill-wizard
intent: "[core capability statement]"
scope: "[single | moderate | extended]"
mechanism: "[reasoning | scripts | hybrid]"
context_assets: "[none | schema | templates | checklists | manuals]"
target_path: "[workspace-relative path ending with /]"
tier: "[A | B | C]"
workflow_notes:
  - "[step -> script|AI -> output or planning constraint]"
turns:
  - turn: 1
    question: "[what was asked]"
    answer: "[user answer]"
    timestamp: "ISO-8601"
draft_changes:
  - "[forge-added draft note, optional]"
example_placed: "[inline | references/Example.md]"
example_generated: false
completed: false
# Fields added by skill-plan (not in skill-forge baseline):
coverage:
  agentskills_io_mandatory:
    name: true
    description: true
  essential_schema:
    intent: true
    scope: true
    mechanism: true
    context_assets: true
    tier: true
    target_path: true
    workflow_notes: true
    example_placed: true
    example_generated: true
unanswered_branches: []
last_backtrack_turn: 0
```

## References

- agentskills.io specification - https://agentskills.io/specification
