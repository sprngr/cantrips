# Pattern Index

Edge case triggers and rare branch conditions. Supplement to SKILL.md pattern matching rules. Consult when standard branches don't match user's answer.

## Edge Cases by Branch

### Branch 1: Intent Clarification

| Edge Case | Signal | Action |
|--|--|--|
| User gives a single word ("linting") | No verb, no object | Ask: "What does linting do in your context? What input → what output?" |
| User describes a meta-skill | "skill that makes skills", "generate skills" | Flag overlap with skill-forge/skill-plan. Ask if they want to extend existing or build new. |
| User wants to wrap an existing tool | "just call eslint", "run prettier" | Probe: is this a thin wrapper (scope: single) or does it add logic around the tool (moderate+)? |
| Intent matches existing skill in workspace | Same verbs/domain as installed skill | Warn: "Existing skill X does similar. Extend it or create new?" |

### Branch 2: Scope Probing

| Edge Case | Signal | Action |
|--|--|--|
| User says "medium" or "not too big" | Vague sizing language | Map to concrete: "Is it 2-5 coordinated steps? Or one action with options?" |
| Scope depends on mechanism choice | "Simple if AI, complex if scripts" | Lock mechanism first (swap branch order). Then revisit scope. |
| User describes conditional scope | "Sometimes 2 steps, sometimes 5" | Ask for the typical/default case. Worst-case goes to workflow_notes. |

### Branch 3: Mechanism Detection

| Edge Case | Signal | Action |
|--|--|--|
| User wants LLM to write scripts at runtime | "AI generates the code then runs it" | This is hybrid. AI reasoning produces scripts, scripts execute. Confirm. |
| User insists on "no AI" | "Pure scripts, no LLM" | Valid but unusual for a skill. Confirm: "The skill instructions still guide AI behavior. Scripts handle logic. OK?" |
| User wants multiple script languages | "Python for parsing, bash for glue" | Fine. Note in workflow_notes. Each script self-contained per spec. |

### Branch 4: Context Asset Discovery

| Edge Case | Signal | Action |
|--|--|--|
| User wants to reference external URLs | "It reads the API docs at runtime" | Not a context_asset (those are static). Note as workflow step. Set context_assets: none unless static copy needed. |
| User has large reference corpus | "50 pages of spec" | Flag progressive disclosure concern. Suggest splitting into focused reference files. |
| User confuses assets with scripts | "A template that runs" | Clarify: assets are static (read-only). If it executes → scripts/. |

### Branch 5: Pipeline Decomposition

| Edge Case | Signal | Action |
|--|--|--|
| Steps have circular dependencies | "A depends on B, B depends on A" | Flag. Ask user to break the cycle. One must come first. |
| User can't enumerate steps | "I don't know the steps yet" | Offer starter patterns based on mechanism: reasoning → (read → analyze → output), scripts → (validate → transform → report). Let user adapt. |
| Steps cross skill boundaries | "Step 3 calls another skill" | Valid for tier C orchestration. Note as workflow_note. Flag that skill-forge will need to handle cross-skill references. |

### Branch 6: Multi-Role Detection

| Edge Case | Signal | Action |
|--|--|--|
| Roles are implicit | "Admin configures, users consume" | Confirm roles explicitly. Ask if skill behavior changes per role. If not → single role, note admin config in workflow_notes. |
| Role = CI/CD system | "GitHub Actions runs this" | Not a human role. This is an environment constraint. Move to compatibility or workflow_notes. |
| User describes approval workflows | "Manager must approve before deploy" | Human-in-the-loop pattern. Flags potential for scripts (gate logic) or external integration. Probe mechanism implications. |

### Branch 7: Hybrid Boundary

| Edge Case | Signal | Action |
|--|--|--|
| Every step is hybrid | "AI decides, then script runs, for every step" | Simplify: is the AI decision the same pattern each time? If yes → one reasoning wrapper + multiple scripts. |
| User can't draw the line | "I'm not sure what should be AI vs script" | Offer heuristic: "If deterministic (same input → same output) → script. If judgment needed → reasoning." |
| User wants AI to validate script output | "AI checks if the script worked" | Valid hybrid pattern. Note boundary: script produces → AI validates → AI reports. |

### Branch 8: Target Path Resolution

| Edge Case | Signal | Action |
|--|--|--|
| User wants global install | "Install for all projects" | Skill lives in `~/.config/opencode/skills/` not workspace. Confirm. Adjust target_path. |
| Path contains skill-forge output | Existing SKILL.md at target | Warn collision. Options: rename, overwrite (explicit yes), different path. |
| User wants nested skill directory | "skills/ci/linting/commit-check/" | Valid but deep. Confirm this is intentional. |

### Branch 9: Example Strategy

| Edge Case | Signal | Action |
|--|--|--|
| User wants no example | "Skip the example" | Set example_placed to inline, example_generated to false. Note: skill-forge may still generate one. |
| User wants multiple examples | "Show a simple and complex case" | Primary example follows tier rule. Additional examples → workflow_notes for skill-forge to handle. |
| Example would expose secrets | Domain involves API keys, credentials | Flag: example must use placeholder values. Note in workflow_notes. |

### Branch 10: Workflow Refinement

| Edge Case | Signal | Action |
|--|--|--|
| User adds major new capability | "Oh, and it should also deploy" | This is scope creep (see anti-patterns). Ask: "New skill or add to workflow_notes?" |
| User contradicts earlier decision | "Actually it should be reasoning, not scripts" | Trigger backtrack to the contradicted branch. Don't just edit — invalidate downstream. |
| User says "done" before coverage complete | Force-exit signal | Write `.skill-plan.yaml` with `completed: false`. List uncovered fields. |

## Rare Compound Patterns

These combine multiple branches in unusual ways:

| Pattern | Branches Involved | Handling |
|--|--|--|
| **Skill-that-orchestrates-skills** | 1 (meta-intent) + 5 (pipeline) + 6 (roles) | Tier C. Each orchestrated skill = a workflow step. Cross-skill references in workflow_notes. |
| **Conditional-everything** | 3 (mechanism) + 7 (hybrid) + 5 (pipeline) | Many conditionals → push to scripts aggressively. Keep SKILL.md as orchestrator only. |
| **AI-generates-then-validates** | 3 (mechanism) + 7 (boundary) | Two-phase hybrid: reasoning phase (generate), script phase (validate), reasoning phase (report). |
| **Tiny-but-scripted** | 2 (scope: single) + 3 (mechanism: scripts) | Tier A but with scripts/. Unusual combo. Confirm user really means single scope with scripts. May be moderate. |
| **Extended-but-reasoning-only** | 2 (scope: extended) + 3 (mechanism: reasoning) | Tier C but no scripts. Orchestrator SKILL.md + stage playbooks in references/. Valid but rare. |
