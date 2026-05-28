---
name: skill-eval
description: Create and run skill evaluations aligned with the agentskills.io eval spec.
  Handles test case authoring, dual-run execution (with/without skill), assertion grading,
  benchmark aggregation, pattern analysis, and improvement iteration. Use when "eval skill",
  "run evals", "skill evaluation", "benchmark skill", or "eval iteration".
---
# Skill Eval

Orchestrate the full evaluation lifecycle for agentskills.io skills.

## Quick start

```
Agent: "eval my-new-skill"
```

The agent authors 2-3 test cases, scaffolds a workspace, runs with-skill and without-skill baselines, grades outputs, and produces a benchmark report.

## Workflows

### 1. Author test cases

1. Read target skill `SKILL.md`. Extract capabilities and constraints.
2. Load `references/test-quality-checklist.md`.
3. Generate 2-3 test cases. Cover normal prompt, edge case, and malformed input.
4. Write test cases to `<target-skill>/evals/evals.json`. Conform to `assets/evals-schema.json`. Produce JSON with keys `skill_name`, `evals[]`. Each eval has `id`, `prompt`, `expected_output`, optional `files[]`.
5. Create input fixture files in `<target-skill>/evals/files/`.
6. Validate `evals.json` against the test quality checklist. Fix flagged items.

### 2. Scaffold workspace

7. Run `scripts/scaffold-workspace.sh <workspace-dir> <iteration-N> <evals-json>`. Script creates per-eval `with_skill/outputs/` and `without_skill/outputs/` directories.
8. Copy current skill to `<workspace>/skill-snapshot/`. Overwrite existing snapshot.

### 3. Execute eval runs

9. Read `references/grading-prompt-template.md`.
10. Spawn a subagent for each `with_skill` run. Pass skill snapshot path, test prompt, input files, and output directory.
11. Save `with_skill/timing.json` on each subagent return.
12. Spawn a subagent for each `without_skill` run. Same prompt, no skill path.
13. Save `without_skill/timing.json` on each subagent return.
14. Verify every eval directory has output files in both `with_skill/outputs/` and `without_skill/outputs/`.

### 4. Grade outputs

15. Run `scripts/grade-assertions.sh <output-dir> <assertions-file>`. Script checks deterministic assertions. Returns partial grading JSON with PASS/FAIL and evidence.
16. Spawn a grading subagent for remaining assertions. Pass outputs and assertion text. Require concrete evidence per result.
17. Save grading results to `<eval-dir>/<config>/grading.json`.

### 5. Aggregate benchmarks

18. Run `scripts/aggregate-benchmark.sh <workspace>/iteration-N`. Compute mean pass rate, token count, and duration. Write delta to `benchmark.json`.
19. Read `assets/eval-report-template.html`. Fill template variables with benchmark data.
20. Write report to `<workspace>/iteration-N/eval-report.html`.

### 6. Analyze patterns

21. Read `references/iteration-playbook.md`.
22. Classify assertions: always-pass, always-fail, skill-dependent, inconsistent.
23. Review execution transcripts for failed evals. Locate skipped instructions and wasted steps.

### 7. Produce improvement recommendations

24. Collect failure signals: failed assertions, human feedback, transcript patterns.
25. Generate skill-forge improvement prompt. Format as YAML with `skill_path`, `iteration`, `benchmark_delta`, and `changes[]` array. Each change has `type`, `section`, `reason`, `suggestion`.
26. Print improvement prompt for user to feed into skill-forge.
27. On user confirmation, loop to step 7 with new iteration number.

## Reference files

See [grading-prompt-template.md](references/grading-prompt-template.md) for LLM judge dispatch prompt.
See [blind-compare-prompt.md](references/blind-compare-prompt.md) for blind comparison scoring.
See [test-quality-checklist.md](references/test-quality-checklist.md) for test case quality review criteria.
See [workspace-layout.md](references/workspace-layout.md) for eval workspace directory structure.
See [iteration-playbook.md](references/iteration-playbook.md) for iteration analysis guidance.
See [eval-report-template.html](assets/eval-report-template.html) for the HTML report template.
