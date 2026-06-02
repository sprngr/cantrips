# Prompt Examples (Generation Phase)

Examples for skill-forge after planning is complete. skill-forge consumes `.skill-plan.yaml` and generates artifacts; it does not run discovery interviews.

### Import Success
```
📥 Imported plan: /workspace/skills/commit-linter/.skill-plan.yaml

Intent: Lint commit messages for Conventional Commits compliance and secret leaks
Scope: moderate
Mechanism: scripts
Tier: B
Target: skills/commit-linter/

Proceed to generate bundle? [yes/no]
```

### Import Failure: Missing Keys
```
⚠️ Plan import failed. Missing required keys: target_path, tier

skill-forge only compiles completed plans.
Patch `.skill-plan.yaml` via skill-refine or rerun skill-wizard/skill-plan,
then rerun /skill-forge.
```

### Import Failure: Incomplete Plan
```
⚠️ Plan is not marked complete (`completed: false`).

Finish planning first, then rerun /skill-forge.
```

### Blueprint Verification
```
┌── Blueprint ───────────────────────────────────────
│ Target: skills/commit-linter/
│
│ skills/commit-linter/
│   SKILL.md
│   scripts/
│     cc-format.sh
│     secret-scan.sh
│   references/
│     Example.md
│     cc-types-checklist.md
└────────────────────────────────────────────────────

SKILL.md preview:
---
name: commit-linter
description: >
  Lints commit messages and flags secret leaks.
---

Generate this bundle? [yes / no]
```

### Plan-Semantic Change Request (Redirect)
```
You requested scope/mechanism changes (moderate scripts → extended hybrid).

skill-forge does not mutate planning decisions.
Patch `.skill-plan.yaml` via skill-refine or rerun skill-wizard/skill-plan,
then rerun /skill-forge.
```

### Draft Quality Gate
```
Running draft validation...
  ❌ "You might want to" → hedging removed
  ❌ "if exists, else create" → conditional wall pushed to scripts/merge.sh
  ✅ Imperative verb-first
  ✅ No instruction >2 lines
  ✅ Relative file paths

Draft corrected. Write to disk? [yes / no / edit]
```

### Full Walkthrough: Plan → Bundle

### User prompt
```
/skill-forge use skills/commit-linter/.skill-plan.yaml
```

### Agent
```
📥 Imported plan: skills/commit-linter/.skill-plan.yaml
Intent: Lint commit messages for Conventional Commits compliance and secret leaks
Scope: moderate
Mechanism: scripts
Tier: B
Target: skills/commit-linter/

Proceed to generate bundle? [yes/no]
```

### User
```
yes
```

### Agent
```
Blueprint ready:
- SKILL.md
- scripts/cc-format.sh
- scripts/secret-scan.sh
- scripts/suggest-fix.sh
- references/cc-types-checklist.md
- references/Example.md

Generate this bundle? [yes/no]
```

### User
```
yes
```

### Agent
```
Running draft validation...
  ❌ Step 6 had conditional wall → moved to scripts/commit-msg-hook.sh
  ✅ Clarity checklist passed

Example generated at references/Example.md.
Write to disk at skills/commit-linter/? [yes/no]
```

### User
```
yes
```

### Agent
```
Writing SKILL.md                                      ✅
Writing scripts/cc-format.sh                          ✅
Writing scripts/secret-scan.sh                        ✅
Writing scripts/suggest-fix.sh                        ✅
Writing scripts/commit-msg-hook.sh                    ✅
Writing references/cc-types-checklist.md              ✅
Writing references/Example.md                         ✅
Updating .skill-plan.yaml metadata                    ✅

🔥 Skill forged.
```

### Agent-calibration notes
- **Tone:** Direct. No interview chatter.
- **Pacing:** Confirm at import, blueprint, and write gates.
- **Boundary:** Semantic plan changes are redirected upstream.
- **Validation:** Anti-pattern and clarity gates run before any write.
