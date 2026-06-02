# Eval Setup Quality Scorecard

Source: https://agentskills.io/skill-creation/evaluating-skills

Score each item: YES = 1, NO = 0. Total / count = eval readiness %.

## Test case design

- [ ] evals/ directory exists
- [ ] evals/evals.json present
- [ ] At least 2–3 test cases defined
- [ ] Test prompts vary in phrasing, detail level, and formality
- [ ] At least one edge-case test included
- [ ] Test prompts use realistic context (file paths, column names)
- [ ] Each test case has an expected_output field

## Assertions

- [ ] Assertions are specific and observable
- [ ] Assertions are programmatically verifiable where possible
- [ ] No vague assertions ("the output is good")
- [ ] No brittle assertions ("uses exactly the phrase...")

## Eval workspace

- [ ] Workspace structure follows iteration-N/ pattern
- [ ] Each eval has with_skill/ and without_skill/ subdirs
- [ ] Timing data captured (timing.json per run)
- [ ] Grading data captured (grading.json per run)
- [ ] Benchmark aggregation file (benchmark.json) produced

## Iteration loop

- [ ] Baseline run exists (without skill or previous version)
- [ ] Results compared with-skill vs without-skill
- [ ] Failed assertions analyzed for root cause
- [ ] Always-passing assertions removed or replaced
- [ ] Human review feedback captured

## Execution traces

- [ ] Agent traces reviewed (not just final output)
- [ ] Wasted work identified and instructions trimmed
- [ ] Bottleneck evals identified (high stddev in timing)

## Scoring guide

- **0–25%**: No evals. Skill is untested. Add evals/evals.json immediately.
- **26–50%**: Partial evals. Add assertions and baseline runs.
- **51–75%**: Good eval setup. Focus on iteration loop and trace review.
- **76–100%**: Mature evals. Skill ready for production iteration.
