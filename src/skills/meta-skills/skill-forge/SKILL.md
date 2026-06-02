---
name: skill-forge
description: >
  Use when a completed `.skill-plan.yaml` (or `.skill-plan.patched.yaml`) is
  ready to generate or update a spec-compliant skill bundle via /skill-forge.
---

Compile a completed `.skill-plan.yaml` into a final, schema-compliant skill bundle.
Do not run discovery interview loops inside skill-forge.

## Core Concepts
* **Plan as Source of Truth:** `.skill-plan.yaml` drives all generation decisions.
* **Generation-Only Contract:** Discovery happens in skill-wizard + skill-plan.
* **Human Write Gate:** Always require explicit confirmation before writing files.
* **Draft Quality Gate:** Enforce anti-pattern and clarity checks before synthesis.

## State Machine

### 0. Import Plan (Required)
* Auto-trigger: User provides a path containing `.skill-plan.yaml` or asks to forge from plan.
* **Action:**
  1. Run `Bash scripts/import-plan.sh <plan-path>` from skill directory.
  2. Parse JSON output into working state (intent, tier, mechanism, target path, notes).
  3. Handle non-zero exits:
     - `1`: plan file missing/unreadable → ask for valid path.
     - `2`: YAML parse/shape error → ask user to repair plan YAML.
     - `3`: required keys missing → list missing keys, ask user to patch via skill-plan/skill-refine.
     - `4`: `completed` is not `true` → stop and ask user to complete planning first.
  4. Print summary: intent, scope, mechanism, tier, target path.
  5. Ask: `Proceed to generate bundle? [yes/no]`

### 1. Blueprint (Verification)
* Build file plan from plan fields (`tier`, `mechanism`, `context_assets`, `workflow_notes`).
* Show projected directory tree + 3-line SKILL.md preview.
* Ask confirmation.
* If user requests structural changes (intent/scope/mechanism/context/path/workflow), do **not** interview or mutate plan inline.
  - Instruct user to patch `.skill-plan.yaml` via skill-refine (or rerun skill-wizard/skill-plan), then rerun skill-forge.

### 2. Draft (Quality Gate)
* Draft SKILL.md instructions using `assets/skill-template.md` as skeleton.
* Generate draft files for `scripts/`, `references/`, and `assets/` based on tier and mechanism.
* Scan draft against anti-patterns below. Print violations to user. Fix internally.
* **Conditional push rule:** If conditional wall cannot be flattened, push logic to `scripts/`. Replace SKILL.md step with one script call. Record change in `draft_changes[]`.
* Run draft against clarity checklist below. Print remaining failures. Fix internally.
* Show corrected draft. Ask: `Write to disk or adjust?`
* If requested adjustment changes plan semantics, stop and route user to patch plan upstream.

### 3. Example (Calibration)
* Generate end-to-end example showing generated skill behavior in use.
* **Placement rule:** Tier A → embed as `## Example` inside SKILL.md. Tier B/C → write to `references/Example.md`.
* **Content rules:**
  - Use realistic user input matching frontmatter triggers.
  - Walk through each workflow step from generated SKILL.md.
  - Include at least one edge case or correction (e.g., conditional push, validation failure).
  - End with concrete output produced by the generated skill.
  - Add `### Agent-calibration notes` block (tone, pacing, output shape).
* Ask: `Example looks good? [yes / no / edit]`
* Persist `example_placed` + `example_generated: true` in plan.

### 4. Write (Synthesis)
* Check target path. Warn on collision. Require explicit yes to overwrite.
* Write files via `Write` tool: SKILL.md, then `scripts/`, `references/` (including `Example.md` if Tier B/C), `assets/` per tier.
* Update `.skill-plan.yaml` metadata:
  - append `draft_changes[]` from quality gate
  - set `example_placed`
  - set `example_generated: true`
  - keep `completed: true`
* Say: `Skill forged.`

#### Gotchas: Anti-Patterns (enforce during drafting)
* ❌ "Consider doing X" → Replace with "Do X."
* ❌ "You might want to..." → Remove. Hard requirement or drop.
* ❌ "This helps with..." → Context. Move to description frontmatter.
* ❌ Long prose paragraphs (>3 sentences) → Break to bullets.
* ❌ "First, second, finally" → Redundant with numbered list. Drop ordinals.
* ❌ Nested lists >2 levels deep → Flatten or split to reference file.
* ❌ "See below/above" → Use file paths or section headers.
* ❌ Conditional walls → Push logic into `scripts/`. Replace step with script call.
* ❌ Repeating frontmatter in body → Delete. Description belongs in YAML only.
* ❌ Open-ended tasks → Add concrete scope constraint.

#### Clarity Checklist (pass all before write)
1. Every instruction is imperative verb-first ("Read", "Generate", "Call")
2. No instruction exceeds 2 lines
3. No hedging words (consider, might, perhaps, optionally, you could)
4. Steps are ordered. If order irrelevant, label as "parallel"
5. Each step has a single verb. No compound actions.
6. File references use relative paths from skill root
7. No vague instruction without a scope constraint
8. Output expectations stated per step ("produce JSON with keys...")
9. Total instruction lines <= 80 (reserve 20 for frontmatter + headers)
10. If step requires external tool, tool name is explicit

### Tier Output Map
| Tier | Output |
|------|--------|
| A | `SKILL.md` (example inline as `## Example`) |
| B | `SKILL.md` + `scripts/*` + `references/Example.md` + `references/*` (if context=yes) |
| C | `SKILL.md` orchestrator + `references/Example.md` + `references/*.md` per stage playbook |

## Reference Files
* `assets/skill-template.md` — SKILL.md skeleton for generated skills
* `assets/plan-template.yaml` — `.skill-plan.yaml` input contract
* `references/Examples.md` — Generation-phase prompt examples
