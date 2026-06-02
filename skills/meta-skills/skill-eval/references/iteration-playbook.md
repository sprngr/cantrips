# Iteration Playbook
## Purpose
Guidance for analyzing eval results between iterations. Read before step 19 (analyze patterns).

## Phase 1: Benchmark triage
Read `benchmark.json`. Answer these questions before touching SKILL.md.

### Pass rate
- Is with_skill delta > 0? If not, the skill adds no measurable value yet.
- Is delta > 10 percentage points? That signals meaningful improvement.
- Pass rate < 0.5 with skill? Skill instructions misaligned with test cases. Debug before iterating.

### Token / time cost
- Token delta > 2x baseline? Skill is expensive. Look for wasted steps in transcripts.
- Time delta < 0? Skill saved time. Rare but possible if instructions prune exploration.

## Phase 2: Per-assertion analysis
Gather all `grading.json` files. Classify each unique assertion text:

| Classification | Meaning | Action |
|---|---|---|
| Always pass (both configs) | Too easy. Remove. | Delete from evals.json |
| Always fail (both configs) | Too hard or broken. Fix. | Rewrite assertion or drop test case |
| Pass with-skill, fail without | **High signal**. Skill value. | Keep. Understand which SKILL.md line caused this. |
| Inconsistent (high stddev) | Flaky eval or ambiguous instruction | Add examples to SKILL.md or tighten assertion |

## Phase 3: Transcript review
Open execution transcripts for failed evals. Look for:

- **Skipped instructions**: model ignored a step. Instruction may be buried, vague, or contradictory.
- **Wasted work**: model spent tokens on irrelevant exploration. Add guardrails or prune ambiguous steps.
- **Repetition**: model wrote the same helper code across runs. Extract to `scripts/`.

## Phase 4: Improvement generation
Collect signals into three buckets:

1. **Failed assertions** → specific gaps. Each maps to a missing step, unclear instruction, or unhandled edge case.
2. **Human feedback** → quality issues. Structural, stylistic, or scope problems.
3. **Transcript patterns** → why things broke. Ambiguity, waste, or instruction ordering issues.

Format as structured improvement prompt for skill-forge:
```yaml
skill_path: <path>
iteration: <N>
benchmark_delta: {pass_rate: X, tokens: Y, time: Z}
changes:
  - type: add|remove|modify
    section: <SKILL.md heading>
    reason: <cited failure pattern>
    suggestion: <concrete replacement text>
```

## Phase 5: Rerun or stop
- Loop if delta < 0.10 and transcript shows fixable issues
- Stop when feedback is consistently empty and delta plateaus
- Stop when adding instructions no longer improves pass rate (over-constrained)
