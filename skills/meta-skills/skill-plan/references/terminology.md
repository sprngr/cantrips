# Terminology

agentskills.io term map. Use these definitions during interview to stay precise. If user uses a synonym, map to canonical term and confirm.

## Spec-Level Terms (agentskills.io)

| Term | Definition | User Synonyms |
|--|--|--|
| **skill** | Directory with SKILL.md + optional scripts/references/assets. Unit of agent capability. | plugin, module, extension, tool |
| **SKILL.md** | Required file. YAML frontmatter (name, description) + Markdown instructions. | skill file, config, manifest |
| **name** | Frontmatter field. Lowercase, hyphens, 1-64 chars. Must match directory name. | id, slug, identifier |
| **description** | Frontmatter field. What skill does + when to use. Max 1024 chars. Must include `Use when` triggers. | summary, about, purpose |
| **scripts/** | Optional directory. Executable code agents can run. Self-contained, clear errors. | code, executables, automation |
| **references/** | Optional directory. Docs agents read on demand. Keep focused and small. | docs, guides, supplemental |
| **assets/** | Optional directory. Static resources: templates, schemas, data files. | resources, static, templates |
| **progressive disclosure** | Load pattern: metadata first (~100 tokens), then SKILL.md body (<5000 tokens), then resources as needed. | lazy loading, on-demand |
| **frontmatter** | YAML block between `---` fences at top of SKILL.md. Contains name, description, optional fields. | header, metadata, config block |
| **compatibility** | Optional frontmatter field. Environment requirements (products, packages, network). | requirements, prerequisites, deps |
| **allowed-tools** | Optional frontmatter field. Pre-approved tools (experimental). | permissions, tool access |

## skill-plan Schema Terms

| Term | Definition | Valid Values |
|--|--|--|
| **intent** | User's core purpose statement for the skill. 1-2 sentences, ≥1 concrete verb. | freeform text |
| **scope** | Complexity level of the skill's workflow. | `single` · `moderate` · `extended` |
| **mechanism** | What powers the skill's logic. | `reasoning` · `scripts` · `hybrid` |
| **context_assets** | Static reference material the skill needs. | `none` · `schema` · `templates` · `checklists` · `manuals` |
| **tier** | Output structure tier. Derived from scope. | `A` (single) · `B` (moderate) · `C` (extended) |
| **target_path** | Where to write the skill. Workspace-relative, no spaces, trailing `/`. | path string |
| **workflow_notes** | Freeform refinements: step ordering, dependencies, role notes, boundary mappings. | list of strings |
| **example_placed** | Where the example goes. Tier A → inline, Tier B/C → references. | `inline` · `references/Example.md` |
| **example_generated** | Whether example placement has been decided. | `true` · `false` |
| **completed** | Review gate passed. YAML finalized. | `true` · `false` |
| **coverage** | Tracking block. Mirrors essential_schema fields + unanswered_branches. | object |
| **turns** | Interview log. Each entry: turn index, answer, timestamp. | list of objects |
| **draft_changes** | Changes made during interview (e.g., conditional pushes to scripts). | list of strings |
| **last_backtrack_turn** | Index of most recent fork point used for backtrack. 0 = no backtrack. | integer |
| **unanswered_branches** | Pending pattern branches not yet resolved. Must be empty for stop condition. | list of strings |

## Tier ↔ Scope ↔ Output Mapping

| Scope | Tier | Output Structure |
|--|--|--|
| single | A | `SKILL.md` only (example inline as `## Example`) |
| moderate | B | `SKILL.md` + `scripts/*` + `references/Example.md` + `references/*` |
| extended | C | `SKILL.md` orchestrator + `references/Example.md` + `references/*.md` per stage |

## Common Misuses to Correct

| User Says | They Probably Mean | Correct Term |
|--|--|--|
| "I want a plugin" | skill | skill |
| "The AI part" | reasoning mechanism | mechanism: reasoning |
| "The code part" | scripts mechanism | mechanism: scripts |
| "Both AI and code" | hybrid mechanism | mechanism: hybrid |
| "Put it in docs/" | references/ directory | references/ (not docs/) |
| "Config file" | SKILL.md or assets/ template | clarify: frontmatter vs asset |
| "Simple skill" | scope: single, tier A | confirm: truly 1 action? |
| "Big skill" | scope: extended, tier C | confirm: multi-stage orchestration? |
