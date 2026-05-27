# Prompt Examples

### Initialization
```
🛠️ The Forge is hot. Let's hammer out a new skill using the agentskills.io standard.

To begin the blueprint, what is the ultimate capability or "superpower" you want this AI to possess?
```

### Decision Log (Mid-Interview)
```
┌── Decision Log ──────────────────────────────────────────┐
│ Intent: Auto-generate daily release notes from git diffs │
│ Scope: moderate pipeline (2-5 steps)                     │
│ Mechanism: [pending]                                     │
└──────────────────────────────────────────────────────────┘

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
