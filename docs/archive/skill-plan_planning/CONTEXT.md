# Goal
- Plan and architect a skill-wizard agent and skill-plan skill as the planning entry point before skill-forge generation.
Constraints & Preferences
- Output must be a .skill-plan.yaml file for skill-forge to consume.
- Must include an approve/deny/edit review gate before writing the YAML.
- Dynamic pattern matching instead of a fixed turn tree.
- Guardrail: exactly 1 follow-up question per answer.
- Stop condition based on a coverage checklist (agentskills.io mandatory + essential schema fields).
- Review output limited to .skill-plan.yaml only.
- Agent and skill must remain separate entities.
- Development copy placed in /mnt/f/workspace/cantrips/skills/meta-skills/skill-plan/ and /mnt/f/workspace/cantrips/agents/.

# Progress

## Done
- Defined delta vs grill-me and skill-forge (domain-specific schema knowledge instead of generic probing).
- Established pipeline: skill-wizard → tiered interview (quick/deep) → .skill-plan.yaml → skill-forge generation.
- Set review gate mechanics (approve/deny) and nearest-fork backtrack on deny.
- Defined pattern matching strategy (8-10 branches in SKILL.md, edge cases in references/pattern-index.md).
- Finalized naming (skill-wizard agent, skill-plan skill).
- Agreed on single planning entry point via skill-wizard; no direct discovery in skill-forge.

## In Progress
- Updating /mnt/f/workspace/cantrips/skills/meta-skills/skill-plan/PLAN.md with the agreed architecture and constraints.

## Blocked
- (none)

## Key Decisions
- Architecture: Split into skill-wizard agent (state/routing/YAML I/O) and skill-plan skill (patterns/glossary/validation).
- Routing: skill-wizard is planning entry point; agent selects quick (simple) or deep (complex) interview depth.
- State Management: skill-wizard reads/writes /mnt/f/workspace/cantrips/skills/meta-skills/skill-plan/.skill-plan.yaml.
- Pattern Matching: 8-10 rules in SKILL.md, glossary in references/terminology.md to keep model on track.
- Schema: Extended agentskills.io schema includes workflow_notes, draft_changes, example_placed, example_generated, completed.

## Next Steps
- Keep skill-wizard and skill-plan docs in sync with quick/deep tiering changes.
- Ensure skill-forge contract remains generation-only from completed `.skill-plan.yaml`.
- Run npx skills add for local installation testing.

## Critical Context
- skill-forge is generation-only and consumes completed `.skill-plan.yaml`.
- grill-me provides generic design interrogation; this new skill provides domain-specific agentskills.io schema intelligence.
- The system relies on /mnt/f/workspace/cantrips/agents/rubber-duck.agent.md as an existing precedent for Agent + Skill architecture in the workspace.
- YAML structure includes turns[] log, scope, mechanism, tier, workflow_notes, and completed flag.

## Relevant Files
- /mnt/f/workspace/cantrips/skills/meta-skills/skill-plan/PLAN.md: Master plan document.
- /mnt/f/workspace/cantrips/skills/meta-skills/skill-forge/SKILL.md: Reference for existing state machine and interview flow.
- /mnt/f/workspace/cantrips/skills/meta-skills/skill-plan/assets/plan-template.yaml: Local YAML planning-state template.
- /mnt/f/workspace/cantrips/skills/meta-skills/skill-forge/references/Examples.md: Reference for prompt formatting and RPG flavor.
- /mnt/f/workspace/cantrips/skills/meta-skills/skill-plan/: Target directory for the new skill development.
- /mnt/f/workspace/cantrips/agents/: Target directory for the new skill-wizard.agent.md file.
- /home/sprngr/.agents/skills/grill-me/SKILL.md: Reference for existing generic interview logic to avoid duplication.

## References
- https://agentskills.io/specification: Agentskills.io specification documentation.
- https://opencode.ai/docs/agents: Opencode agents configuration documentation.
