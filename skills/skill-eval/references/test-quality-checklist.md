# Test Case Quality Checklist
## Usage
Run this checklist against every evals.json before launching runs. Fix flagged items.

### Coverage
- [ ] At least 2 test cases, maximum 5 for first iteration
- [ ] Normal case: realistic prompt matching target skill's core use case
- [ ] Edge case: boundary condition, malformed input, or ambiguous instruction
- [ ] Stress case: prompt that could reveal ambiguity in skill instructions

### Prompt quality
- [ ] Prompts vary in phrasing, formality, and detail level
- [ ] Prompts use realistic context (file paths, column names, domain terms)
- [ ] No prompt is "process this" or "do the thing" — each has concrete targets
- [ ] Each prompt is self-contained. No missing prerequisites.

### Expected output quality
- [ ] Each `expected_output` is specific. Names the artifact. States structure.
- [ ] No "the output is good" or vaguely positive language
- [ ] Expected output is achievable. The skill can produce it.

### Assertions (if present beyond first iteration)
- [ ] Each assertion is verifiable. Can be checked from output alone.
- [ ] No assertion is too brittle (exact string match on flexible text).
- [ ] No assertion is too easy (always passes regardless of skill quality).
- [ ] Count-based assertions use thresholds ("at least 3"), not fixed counts.

### Fixture files
- [ ] Every `files[]` entry exists at the referenced path
- [ ] Fixture files are realistic (not lorem ipsum or single-row tables)
- [ ] File paths in evals.json match actual fixture locations

### Scoring
- 12+ checks pass: good eval set
- 9-11 checks pass: fix low items before running
- <9 checks pass: redraft test cases
