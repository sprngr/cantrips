# Example: squash end-to-end

## User input
`/squash continue skill-refine and forge flow after report parsing`

## Walkthrough

1. Agent defines scope.
   - Output: `scope: current session decisions + open blockers + next actions`

2. Agent infers next-session focus from user arguments.
   - Output: `focus: continue skill-refine and forge flow after report parsing`

3. Agent generates compact handoff with full-path file references.
   - Output:
     ```md
     ## Goal
     Continue refine-first workflow for squash skill updates.

     ## Decisions
     - Keep plan patches in `.skill-plan.patched.yaml` before forge.
     - Keep bundle edits gated by explicit user approval.

     ## Open questions
     - Confirm which report findings become P0 apply queue.

     ## Next actions
     - Parse latest reports.
     - Rank findings.
     - Propose patch ops.

     ## File references
     - /mnt/f/workspace/cantrips/skills/experimental/squash/.skill-plan.yaml
     - /mnt/f/workspace/cantrips/skills/meta-skills/skill-refine/SKILL.md
     ```

4. Agent adds `Suggested skills` section with reasons.
   - Output includes: `skill-refine`, `skill-forge`, `duck-review` with one-line rationale.

5. Agent redacts sensitive content.
   - Output replaces secrets/PII with `[REDACTED]`.

6. Agent removes duplicate detail covered by referenced artifacts.
   - Output keeps references, drops repeated artifact bodies.

7. Agent rewrites output in caveman-terse style.

8. Agent resolves target path.
   - Output: `target_path: auto-temp` when user did not pass path.

9. Agent calls:
   - `Bash scripts/squash-session.sh` with step-7 text on stdin.
   - Prerequisite: NLTK installed per `references/NLTK-Setup.md`.

10. Script returns saved path.
    - Output: `saved: /tmp/handoff-20260530-153011-A1b2C3.md`

11. Agent reports final handoff + saved path.
    - Output includes: `saved: /tmp/handoff-20260530-153011-A1b2C3.md`

## Edge case: user provides explicit output path
- Input: `/squash output/handoff.md continue forge pass`
- Behavior: use `output/handoff.md`; do not fallback to OS temp dir.

## Concrete output produced
```md
Goal: continue refine-first squash updates.
Decisions: patch plan first. forge after approve.
Open questions: choose p0 findings apply list.
Next actions: parse reports. rank. patch queue.
Suggested skills:
- skill-refine: convert findings into plan patch ops.
- skill-forge: compile approved patched plan.
- duck-review: verify final diff quality.
File refs: /mnt/f/workspace/cantrips/skills/experimental/squash/.skill-plan.yaml
Load context: /mnt/f/workspace/cantrips/skills/experimental/squash/.skill-plan.yaml
Saved: /tmp/handoff-20260530-153011-A1b2C3.md
```

### Agent-calibration notes
- Tone: terse, direct, no discovery chatter.
- Pacing: execute step order; confirm only at write gate.
- Output shape: order fields `Goal`, `Decisions`, `Open questions`, `Next actions`, `Suggested skills`, `File refs`, `Load context`, `Saved`.
