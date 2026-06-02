# Example — Skill Refine (Plan Patch Loop)

End-to-end transcript showing skill-refine turning reports into `.skill-plan.yaml` patch artifacts for skill-forge.

---

## User prompt

```
refine plan skills/commit-linter/.skill-plan.yaml
```

## Turn 1: Load plan + reports

**Agent:**
```
Loaded base plan: skills/commit-linter/.skill-plan.yaml
Found reports:
  - commit-linter-skill-check-report.html
  - iteration-1/eval-report.html

Parsed reports successfully.
Findings: 9 total (P0:2, P1:3, P2:3, P3:1)

Build patch proposals now? [yes / stop]
```

**User:**
```
yes
```

## Turn 2: Propose patch operations

**Agent:**
```
┌── Plan Patch Proposal #1 ─────────────────────────────
│ Priority: P0 — spec violation
│ Source:   skill-check → spec:description_valid
│ Finding:  Generated description too long and vague
│
│ Plan field: workflow_notes
│ Action:     add
│
│ Before:
│   []
│
│ After:
│   - "Description must stay under 1024 chars and include concrete triggers"
│
│ Rationale: Adds hard constraint so forge generates compliant frontmatter.
└───────────────────────────────────────────────────────
[apply / skip / edit / stop]
```

**User:**
```
apply
```

**Agent:**
```
✅ Queued operation op-001.
```

**Agent:**
```
┌── Plan Patch Proposal #2 ─────────────────────────────
│ Priority: P1 — failing eval
│ Source:   skill-eval → test-02/assertion:missing-fix-output
│ Finding:  Workflow lacks explicit output for suggest-fix step
│
│ Plan field: workflow_notes
│ Action:     add
│
│ Before:
│   ["Description must stay under 1024 chars and include concrete triggers"]
│
│ After:
│   - "Description must stay under 1024 chars and include concrete triggers"
│   - "Workflow must state output for suggest-fix step: corrected subject line"
│
│ Rationale: Signals forge to generate explicit output expectation.
└───────────────────────────────────────────────────────
[apply / skip / edit / stop]
```

**User:**
```
edit
```

**User (edited After):**
```
- "Description must stay under 1024 chars and include concrete triggers"
- "Workflow step for suggest-fix must output corrected subject line to stdout"
```

**Agent:**
```
Edited patch accepted. Apply this version? [apply / skip]
```

**User:**
```
apply
```

## Turn 3: Build patch artifacts

**Agent:**
```
Writing patch artifact:
  skills/commit-linter/.skill-plan.patch.yaml

Applying patch queue in memory...
Writing patched plan:
  skills/commit-linter/.skill-plan.patched.yaml

Validating patched plan against forge import contract...
✅ Validation passed (required fields/enums/completed=true)

Changed fields:
  workflow_notes: +2 entries
```

## Turn 4: Handoff

**Agent:**
```
Patch ready.

Use patched plan for generation:
/skill-forge skills/commit-linter/.skill-plan.patched.yaml

Keep base plan unchanged for traceability.
```

---

### Agent-calibration notes

- **Tone:** Direct, proposal-driven.
- **Pacing:** One patch proposal per turn.
- **Boundary:** Plan edits only. No direct SKILL.md/script edits here.
- **Output shape:** ranked findings → patch queue → patch artifact + patched plan → forge handoff.
