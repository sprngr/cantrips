# Prompt Examples

### Initialization
```
🛠️ The Forge is hot. Let's hammer out a new skill using the agentskills.io standard.

To begin the blueprint, what is the ultimate capability or "superpower" you want this AI to possess?
```

### Decision Log (Mid-Interview)
```
┌── Decision Log ─────────────────────────────────────────
│ Intent: Auto-generate daily release notes from git diffs
│ Scope: moderate pipeline (2-5 steps)                    
│ Mechanism: [pending]                                    
└─────────────────────────────────────────────────────────

Next branch: Does this skill need deterministic scripting (Python/shell), or is AI reasoning on log text enough?
[A] Reasoning only   [B] Scripts only   [C] Both hybrid
```

### Backtrack Handling
```
🔄 Correction noted. Unwinding from Turn 3...

Previous mechanism was "reasoning only" → now switching to "hybrid."
Scope and intent remain locked. Re-evaluating downstream...

What scripts should handle the heavy lifting? (e.g., git diff parser, changelog formatter, email sender)
Reply "back" to retreat further.
```

### Clarity Gate (Pre-Write)
```
Running instruction draft against clarity checklist...
  ✅ Imperative verb-first: PASS
  ⚠️  Step 4 exceeds 2 lines → fixed
  ✅ No hedging words: PASS
  ✅ Single verb per step: PASS

Draft corrected. Write to disk at skills/release-notes/? [yes / no / edit first]
```

### Conditional Push to Scripts
```
❌ Step 9: "Append if file exists, or create if missing" → conditional wall detected.
   → Pushing logic to scripts/merge_changelog.py
   → Replacing step with: "Run scripts/merge_changelog.py to append or create CHANGELOG.md."
   → File plan updated: scripts/ now contains merge_changelog.py.
```

### Import Mode (Stub Detection)
```
📥 Detected plan file / stub at skills/my-skill/SKILL.md.
   Parsed intent: Generate unit tests from function signatures
   Parsed scope: moderate pipeline

Pre-filling decision log with detected values. Resume interview from Turn 3?
[yes / start fresh]
```

---

## Full Walkthrough: "Commit Message Linter" Skill

End-to-end transcript. Shows every turn, backtrack, conditional push, and final SKILL.md output. Use to calibrate agent tone, pacing, and output format.

### User prompt
```
/skill-forge I want a skill that reviews my commit messages before they go out.
Checks Conventional Commits format, flags secrets, suggests subject-length fixes.
```

### Turn 1 (Intent)
**Agent:**
```
🛠️ The Forge is hot. Let's hammer out a new skill.

What is the ultimate capability or "superpower" of this skill?
(Summarize in one sentence. We refine later.)
```

**User:**
```
Lint commit messages against Conventional Commits spec, detect secrets/passwords,
and auto-suggest fixes for long subject lines.
```

**Agent → persist to `.skill-plan.yaml`:**
```yaml
intent: "Lint commit messages for Conventional Commits compliance, detect secrets, suggest subject-length fixes"
turns:
  - turn: 1 (intent)
    answer: "Lint commit messages for Conventional Commits compliance, detect secrets, suggest subject-length fixes"
```

---

### Turn 2 (Scope)
**Agent:**
```
┌── Decision Log ──────────────────────────────────────────────
│ Intent: Lint commit messages, detect secrets, fix suggestions
│ Scope: [pending]                                          
└──────────────────────────────────────────────────────────────

How many distinct steps will this skill execute?
[A] Single task (one action)
[B] Moderate pipeline (2–5 steps)
[C] Extended orchestration (multi-stage, multi-file)
```

**User:**
```
B
```

**Agent → persist:**
```yaml
scope: moderate
tier: B
turns:
  - ... (turn 1)
  - turn: 2 (scope)
    answer: "moderate pipeline (2-5 steps)"
```

---

### Turn 3 (Mechanism)
**Agent:**
```
┌── Decision Log ──────────────────────────────────────────────
│ Intent: Lint commit messages, detect secrets, fix suggestions
│ Scope: moderate pipeline (2–5 steps) / Tier B           
│ Mechanism: [pending]                                    
└──────────────────────────────────────────────────────────────

What powers the heavy lifting?
[A] AI reasoning only
[B] Deterministic scripts
[C] Hybrid (reasoning + scripts)
```

**User:**
```
B, I want regex rules and a secret scanner
```

**Agent:**
```
🔄 Locking mechanism to [B] scripts.

What scripts do you need? Name them or describe their job.
(e.g., "cc-check.sh validates format", "secret-scan.py finds keys")
Reply "back" to change scope first.
```

**User:**
```
- cc-format.sh: parse and validate Conventional Commits regex
- secret-scan.sh: grep-like scan for API keys, passwords, tokens
- suggest-fix.sh: truncate or rephrase long subjects
```

**Agent → persist:**
```yaml
mechanism: scripts
turns:
  - ... (turn 1–2)
  - turn: 3 (mechanism)
    answer: "scripts only — cc-format.sh, secret-scan.sh, suggest-fix.sh"
```

---

### Turn 4 (Context)
**Agent:**
```
┌── Decision Log ──────────────────────────────────────────────
│ Intent: Lint commit messages, detect secrets, fix suggestions
│ Scope: moderate pipeline / Tier B                       
│ Mechanism: scripts (cc-format, secret-scan, suggest-fix)     
│ Context assets: [pending]                                
└──────────────────────────────────────────────────────────────

Does this skill need static reference material?
(JSON schema, prompt templates, checklists, spec manifests, etc.)
[yes / no]
```

**User:**
```
yes, a checklist of Conventional Commits types and scopes
```

**Agent → persist:**
```yaml
context_assets: checklists
turns:
  - ... (turn 1–3)
  - turn: 4 (context)
    answer: "checklist of valid Conventional Commits types and scopes"
```

---

### Turn 5 (Target Path)
**Agent:**
```
┌── Decision Log ──────────────────────────────────────────────
│ Intent: Lint commit messages, detect secrets, fix suggestions
│ Scope: moderate / Tier B                                 
│ Mechanism: scripts                                       
│ Context: checklist                                       
│ Target path: [pending]                                   
└──────────────────────────────────────────────────────────────

Where should we save this skill? (workspace-relative path)
```

**User:**
```
skills/commit-linter/
```

**Agent:**
```
Path skills/commit-linter/ is empty. OK to write there? [yes / no]
```

**User:**
```
yes
```

**Agent → persist:**
```yaml
target_path: "skills/commit-linter/"
```

---

### State 3: Blueprint (Verification)
**Agent:**
```
┌── Blueprint ───────────────────────────────────────
│ Target: skills/commit-linter/                      
│                                                    
│ skills/commit-linter/                              
│   SKILL.md                                          
│   scripts/                                          
│     cc-format.sh                                    
│     secret-scan.sh                                  
│     suggest-fix.sh                                   
│   references/                                       
│     cc-types-checklist.md                            
│                                                     
│ SKILL.md preview (truncated):                        
│   ---                                               
│   name: commit-linter                                
│   description: >                                      
│     Lints commit messages for Conventional Commits
│     compliance, detects secrets, suggests fixes.
│   ---                                              
│                                                          
│   ## Workflows                                           
│   1. Read staged commit message...                        
│   2. Run scripts/cc-format.sh...                           
│   3. Run scripts/secret-scan.sh...                        │
└────────────────────────────────────────────────────

Any workflow steps to add, remove, or reorder?
Type step text, or say "looks good."
```

**User:**
```
Add a step between 2 and 3: if cc-format fails, suggest-fix should run
before the user commits.
```

**Agent:**
```
Noted. Inserting suggest-fix branch after cc-format validation.
Workflow updated.

┌── Decision Log (final) ─────────────────────
│ Intent: Lint commit messages, detect secrets
│ Scope: moderate pipeline (Tier B)
│ Mechanism: scripts
│ Context: checklists
│ Target: skills/commit-linter/
│ Workflow notes:
│   - suggest-fix runs on cc-format failure
└─────────────────────────────────────────────

Proceed to draft? [yes]
```

---

### State 4: Draft (Quality Gate)
**Agent → internal draft pass:**
```
Running draft against anti-pattern scan...
  ❌ "You might want to run this before git commit" → hedging detected → REMOVED
  ❌ "First validate format, then scan secrets" → redundant ordinals → flattened
  ❌ "Append if .git/commit-msg exists, else create" → conditional wall → PUSHED

→ Pushing conditional to scripts/commit-msg-hook.sh
→ Replacing step with: "Run scripts/commit-msg-hook.sh to install or update hook."
→ File plan updated: scripts/ now contains commit-msg-hook.sh

Running clarity checklist...
  ✅ Imperative verb-first: PASS
  ✅ No instruction > 2 lines: PASS (was 3, truncated)
  ✅ No hedging words: PASS
  ✅ Single verb per step: PASS
  ✅ Steps ordered: PASS
  ✅ Relative paths: PASS
  ✅ No vague scope: PASS
  ✅ Output expectations stated: PASS
  ✅ Total lines <= 80: PASS (42 lines)
  ✅ External tools named: PASS

All gates passed. Draft ready.
```

**Agent → show final SKILL.md to user:**

```markdown
---
name: commit-linter
description: >
  Lints commit messages for Conventional Commits compliance,
  detects embedded secrets, and suggests subject-length fixes.
  Use when "lint commit", "check commit message", "commit hook", or "/commit-lint".
---
# Commit Message Linter

## Quick start
```bash
# Hook auto-runs on git commit. Manual dry-run:
echo "fix(auth): handle token expiry" | scripts/cc-format.sh
```

## Workflows
1. Read commit message from stdin or .git/COMMIT_EDITMSG.
2. Run `scripts/cc-format.sh <message>` → produce PASS/FAIL + violated rule.
3. On FAIL, run `scripts/suggest-fix.sh <message>` → print corrected subject line.
4. Run `scripts/secret-scan.sh <message>` → print line:col of detected secrets.
5. Produce summary: format status, secret count, suggested fix. Exit 1 if any FAIL.
6. Run `scripts/commit-msg-hook.sh` to install or update git hook. Produce confirmation path.

## Advanced features
See [Conventional Commits Types](references/cc-types-checklist.md)
```

**Agent:**
```
Write to disk at skills/commit-linter/? [yes / no / edit]
```

---

### State 5: Write (Synthesis)
**User:**
```
yes
```

**Agent:**
```
Writing SKILL.md → skills/commit-linter/SKILL.md          ✅
Writing cc-format.sh → skills/commit-linter/scripts/       ✅
Writing secret-scan.sh → skills/commit-linter/scripts/     ✅
Writing suggest-fix.sh → skills/commit-linter/scripts/     ✅
Writing commit-msg-hook.sh → skills/commit-linter/scripts/ ✅
Writing cc-types-checklist.md → references/                ✅
Finalizing .skill-plan.yaml → completed: true              ✅

🔥 Skill forged.
```

### Agent-calibration notes
- **Tone:** Direct. Decision log shown after every turn. No small talk.
- **Pacing:** One question per turn. User answers short. Agent persists immediately.
- **Backtrack:** User corrected workflow in State 3. Agent applied inline, did not rewind turns.
- **Conditional push:** Anti-pattern scan caught "if/else" wall → pushed to script → replaced step.
- **Final output:** Matches `assets/skill-template.md` skeleton. All anti-patterns cleared.
