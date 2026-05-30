---
name: skill-plan
description: >
  Planning knowledge base for skill-wizard's tiered interview.
  Provides pattern matching rules, terminology, and schema validation
  for the skill-wizard agent interview loop.
  Use when: /skill-plan, or when skill-wizard is building/refining `.skill-plan.yaml` before /skill-forge.
---

Domain knowledge for skill-wizard's dynamic interview. Provides pattern branches, terminology map, and planning anti-patterns.

## Pattern Matching Rules

Select next question based on last answer. Match top-to-bottom, first hit wins. If no pattern matches, ask for clarification on the least-covered schema field.

**Global rule:** When presenting options, list all valid choices with equal weight. Never pre-select, narrow to a subset, or end with "this seems like X — agree?" Let the user choose.

### Branch 1: Intent Clarification

**Trigger:** Intent is vague, multi-purpose, or contains >2 distinct verbs.
**Signal words:** "and also", "plus", "everything", "all-in-one"
**Action:** Ask user to pick the single most important capability. Others become workflow_notes.
**Resolves:** `intent`

### Branch 2: Scope Probing

**Trigger:** Intent is clear but scope ambiguous. User hasn't said single/moderate/extended.
**Signal words:** "a few steps", "simple", "complex", "orchestrate", "pipeline"
**Action:** Present scope options with concrete examples:
- Single: "One action, one output" (e.g., format a file)
- Moderate: "2-5 coordinated steps" (e.g., lint → fix → report)
- Extended: "Multi-stage orchestration" (e.g., plan → execute → verify → rollback)
**Resolves:** `scope`, `tier` (derived: single→A, moderate→B, extended→C)

### Branch 3: Mechanism Detection

**Trigger:** Scope resolved. User mentions code, regex, parsing, deterministic logic, or AI judgment.
**Signal words:** "script", "regex", "parse", "deterministic", "AI", "reasoning", "LLM", "judgment"
**Action:** If signal points clearly to one mechanism, confirm. If ambiguous, present options:
- Reasoning: "AI reads input, applies judgment, produces output"
- Scripts: "Deterministic code handles logic (regex, parsers, formatters)"
- Hybrid: "AI orchestrates, scripts handle heavy lifting"
**Resolves:** `mechanism`

### Branch 4: Context Asset Discovery

**Trigger:** Mechanism resolved. Workflow implies external data, schemas, or reference material.
**Signal words:** "spec", "schema", "template", "checklist", "config", "manifest", "reference doc"
**Action:** Ask what static assets the skill needs. Offer categories:
- none: skill is self-contained
- schema: JSON/YAML schema for validation
- templates: document or prompt templates
- checklists: verification lists
- manuals: external documentation to reference
**Resolves:** `context_assets`

### Branch 5: Pipeline Decomposition

**Trigger:** Scope is moderate or extended. Steps not yet enumerated.
**Signal words:** "steps", "stages", "phases", "first...then", "workflow"
**Action:** Ask user to list the concrete steps in order. Each step = one verb + one output.
**Resolves:** `workflow_notes` (partial — steps captured as notes)

### Branch 6: Multi-Role Detection

**Trigger:** Answer mentions different actors, permissions, or audiences.
**Signal words:** "admin", "user", "reviewer", "approver", "CI", "human-in-the-loop"
**Action:** Ask which roles interact with the skill and how. Flag if skill needs role-conditional logic (→ potential scripts push).
**Resolves:** `workflow_notes` (appends role notes), may reopen `mechanism` if roles imply scripting

### Branch 7: Hybrid Boundary

**Trigger:** Mechanism is hybrid. Division between reasoning and scripts unclear.
**Signal words:** "AI decides", "script handles", "conditional", "fallback"
**Action:** Ask: "Which steps need deterministic code and which need AI judgment?" Map each workflow step to reasoning or script.
**Resolves:** `workflow_notes` (appends boundary mapping)

### Branch 8: Target Path Resolution

**Trigger:** All content fields resolved. Location not yet set.
**Signal words:** "save", "where", "path", "directory"
**Action:** Ask where to save. If user unsure, suggest `skills/<skill-name>/` in workspace root. Warn on existing path collision.
**Resolves:** `target_path`

### Branch 9: Example Strategy

**Trigger:** Tier determined. Example placement not decided.
**Action:** Based on tier:
- Tier A → default inline (`## Example` in SKILL.md). Confirm or override.
- Tier B/C → default `references/Example.md`. Confirm or override.
**Resolves:** `example_placed`, `example_generated`

### Branch 10: Workflow Refinement

**Trigger:** All 9 essential fields have values. `unanswered_branches` not empty.
**Action:** Address each remaining branch. Ask 1 question per branch per turn. When branch resolves, remove from `unanswered_branches`.
**Resolves:** clears `unanswered_branches` → triggers stop condition

## Planning Anti-Patterns

Flag these during interview. Do not let them into `.skill-plan.yaml`.

| Anti-Pattern | Detection | Fix |
|--|--|--|
| Kitchen-sink intent | Intent has >3 distinct verbs or "and also" chains | Split. Pick primary. Others → workflow_notes or separate skill. |
| Scope creep mid-interview | User adds major capability after scope locked | Ask: "New skill or add to workflow_notes?" If new → suggest separate plan. |
| Mechanism flip-flop | User changes mechanism >2 times | Pause. Summarize tradeoffs. Ask for final commitment. |
| Phantom scripts | User names scripts but can't describe what they do | Probe: "What does X.sh take as input? What does it output?" No answer → drop. |
| Vague target path | User says "somewhere" or "wherever" | Suggest concrete default. Require explicit confirmation. |
| Over-decomposition | User lists >10 workflow steps for moderate scope | Suggest consolidating related steps. If truly >10 → re-evaluate scope (moderate → extended). |
| Role explosion | User describes >4 distinct roles | Ask which are essential for v1. Defer others to future iteration. |

## Schema Validation Rules

Before review gate (State 2), validate:

1. `intent` is ≤2 sentences. Contains ≥1 concrete verb.
2. `scope` is exactly one of: single, moderate, extended.
3. `mechanism` is exactly one of: reasoning, scripts, hybrid.
4. `context_assets` is exactly one of: none, schema, templates, checklists, manuals.
5. `tier` matches scope (single→A, moderate→B, extended→C).
6. `target_path` is non-empty, contains no spaces, ends with `/`.
7. `workflow_notes` has ≥1 entry if scope is moderate or extended.
8. `example_placed` is exactly one of: inline, references/Example.md.
9. `example_generated` is boolean.

If any fail → flag to user in review gate, ask to fix before approve.

## Reference Files

- [Terminology](references/terminology.md) — agentskills.io term map and field definitions.
- [Pattern Index](references/pattern-index.md) — edge case triggers and rare branch conditions.
