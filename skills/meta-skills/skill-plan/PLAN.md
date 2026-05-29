# skill-plan

A deep planning skill to kick off the agent skill development lifecycle.

## Intent
The function of this skill will be to interview me relentlessly about every aspect of this new skill until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

The results will be written to a .skill-plan.yaml file in the target directory.

This skill will function as the first step before invoking `skill-forge`.

## .skill-plan schema

Original schema design, open to expansion.

```yaml
# .skill-plan.yaml - Auto-generated interview state
intent: "[user's original intent statement]"
scope: "[single | moderate | extended]"
mechanism: "[reasoning | scripts | hybrid]"
context_assets: "[none | schema | templates | checklists | manuals]"
target_path: "[resolved absolute or workspace-relative path]"
tier: "[A | B | C]"
workflow_notes:
  - "[freeform refinement from State 3.5]"
turns:
  - turn: 1 (intent)
    answer: "..."
    timestamp: "ISO-8601"
  - turn: 2 (scope)
    answer: "..."
    timestamp: "ISO-8601"
draft_changes:
  - "[conditional pushed to scripts/fallback_handler.py]"
example_placed: "[inline | references/Example.md]"
example_generated: false
completed: false
```