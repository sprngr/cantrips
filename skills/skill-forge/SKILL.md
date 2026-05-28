---
name: skill-forge
description: >
  Interactive wizard that interviews the user to build a spec-compliant
  agentskills.io skill bundle: SKILL.md, scripts, assets, and references.
  Use when the user wants to create a new skill, or invokes /skill-forge.
---

Guide the user from a raw concept to a compiled, schema-compliant skill bundle via a branching dialogue tree.

## Core Concepts
* **Progressive Disclosure:** One focal question per turn.
* **State Memory:** Persist decision log to `[target]/.skill-plan.yaml` (schema: `assets/plan-template.yaml`). Resume survives drop.
* **Backtrack:** "back"/"undo"/contradiction → invalidate fork + downstream → re-prompt from fork point.
* **Uncertainty:** If user stuck, offer 2-3 starter templates. Let them pick.

## State Machine

### 0. Import (If Triggered)
* **Turn tracking rule:** Ignore pre-filled fields (scope/mechanism/context/path). Only `turns[]` length determines progress.
* Auto-trigger: User says "continue skill" OR names a path containing `.skill-plan.yaml`.
* **Action:**
  1. Run `Bash scripts/import-plan.sh <plan-path>` from skill directory.
  2. Parse KEY=VALUE output. Map `TURNS` → resume turn (TURNS=1 → resume Turn 2, TURNS=2 → resume Turn 3, etc.). If `TURNS=0`, start at Turn 1.
  3. If exit code 4 (`COMPLETED=true`), print summary, say "Skill already complete. Re-forge?", exit if no.
  4. If exit code 3 (missing keys), warn user, print fields still available, ask if they want to continue from here.
  5. Print summary: intent, tier, turns completed, target path. Ask: "Resume interview? (yes/no)"

### 1. Onboarding (Intent)
* Greet with RPG-flavored welcome (see `references/Examples.md` §Initialization).
* Ask: Define the skill's core intent or "superpower."
* **Constraint:** Block all other questions until intent is set.
* Save to `.skill-plan.yaml` → persist.

### 2. Branching (Turns 2–5)
* **Turn 2 (Scope):** Single task | moderate pipeline (2–5 steps) | extended orchestration. Maps to Tier A / B / C.
* **Turn 3 (Mechanism):** Default: [A] AI reasoning (most skills start here). Offer [B] scripts or [C] hybrid only if intent implies scripting. Flags `scripts/` if B or C.
* **Turn 4 (Context):** Static assets? JSON schema? Prompt templates? Checklists? Manifolds? Flags `references/` if yes.
* **Turn 5 (Target Path):** Where to save? If path exists with same-skill name, warn + propose rename. Require explicit yes.

After each turn: show decision log, append to `.skill-plan.yaml`.

### 3. Blueprint (Verification)
* Show: directory tree for selected tier + 3-line SKILL.md preview with real intent filled in.
* Ask confirmation. Corrections → apply backtrack rules.
* Then ask: "Any workflow steps to add, remove, or reorder?" Store as `workflow_notes[]` in plan.
* If refinement changes scope/mechanism → trigger backtrack to Turns 2–3.

### 4. Draft (Quality Gate)
* Draft SKILL.md instructions. Use `assets/skill-template.md` as skeleton.
* Scan draft against the anti-patterns below. Print violations to user. Fix internally.
* **Conditional push rule:** Anti-pattern flags conditional logic that won't flatten → push logic into `scripts/`. Replace SKILL.md step with single script call. Update file plan + `draft_changes[]` in plan.
* Run draft against the clarity checklist below. Print remaining failures. Fix internally.
* Show corrected draft. Ask: "Write to disk or adjust?"

### 4.5. Example (Calibration)
* Generate end-to-end example showing the skill in action. Format: simulated transcript of user prompt → agent Turn 1 → Turn 2 → … → final output.
* **Placement rule:** If Tier A (SKILL.md only), embed example as `## Example` section inside SKILL.md. If Tier B or C, write to `references/Example.md`.
* **Content rules:**
  - Show realistic user input matching the `Use when` triggers from frontmatter.
  - Walk through every workflow step the SKILL.md defines.
  - Include at least one edge case or correction (backtrack, conditional push, refinement).
  - End with the concrete output the skill produces.
  - Add `### Agent-calibration notes` block: tone, pacing, anti-pattern catches, output shape.
* **Reference:** See `references/Examples.md` §Full Walkthrough for format model.
* Ask: "Example looks good? [yes / no / edit]"
* Persist example path + `example_generated: true` to `.skill-plan.yaml`.

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
* ❌ Open-ended tasks → Add scope: "search files matching *.ts."

#### Clarity Checklist (pass all before write)
1. Every instruction is imperative verb-first ("Read", "Generate", "Call")
2. No instruction exceeds 2 lines
3. No hedging words (consider, might, perhaps, optionally, you could)
4. Steps are ordered. If order irrelevant, label as "parallel"
5. Each step has a single verb. No compound actions.
6. File references use relative paths from skill root
7. No vague instruction without a scope constraint
8. Output expectations stated per step ("produce a JSON object with keys...")
9. Total instruction lines <= 80 (reserve 20 for frontmatter + headers)
10. If step requires external tool, tool name is explicit

### 4.5. Example (Calibration)
* Generate end-to-end walkthrough of the skill in action. Match format in `references/Examples.md` §Full Walkthrough.
* **Content:** Simulated transcript: user prompt → Turn 1 intent → Turn 2 scope → … → final output. Include at least one backtrack or anti-pattern catch.
* **Placement:** Tier A → embed as `## Example` section inside SKILL.md. Tier B/C → write to `references/Example.md`.
* Show example. Ask: "Example accurate? [yes / no / edit]"
* Store `example_placed: inline | references/Example.md` + `example_generated: true` in plan.

### 5. Write (Synthesis)
* Check target path. Warn on collision. Require explicit yes to overwrite.
* Write all files via `Write` tool: SKILL.md, then `scripts/`, `references/` (including `Example.md` if Tier B/C), `assets/` per tier.
* Finalize `.skill-plan.yaml` → set `completed: true`.
* Say: "Skill forged."

### Tier Output Map
| Tier | Output |
|------|--------|
| A | `SKILL.md` (example inline as `## Example`) |
| B | `SKILL.md` + `scripts/*` + `references/Example.md` + `references/*` (if context=yes) |
| C | `SKILL.md` orchestrator + `references/Example.md` + `references/*.md` per stage playbook |

## Reference Files
* `assets/skill-template.md` — SKILL.md skeleton for generated skills
* `assets/plan-template.yaml` — `.skill-plan.yaml` schema
* `references/Examples.md` — Prompt examples for each state
