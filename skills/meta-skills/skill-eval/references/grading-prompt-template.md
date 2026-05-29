# Grading Prompt Template
## Usage
Fill variables in braces. Dispatch to a subagent for clean-context execution. Ignore token usage concerns.

## With-Skill Run Template
```
Execute this skill evaluation run:

- Skill path: {SKILL_PATH}
- Task prompt: "{PROMPT}"
- Input files to copy into working directory:
{FILES_LIST}
- Save all outputs to: {OUTPUT_DIR}
- On completion, save timing.json:
  {
    "total_tokens": {TOKEN_COUNT_FROM_AGENT},
    "duration_ms": {DURATION_MS_FROM_AGENT}
  }

Rules:
- Work only from the SKILL.md instructions. Ignore prior context.
- Copy input files before starting.
- Write all produced files into the output directory.
- Do not modify input files in place. Work on copies.
```

## Without-Skill (Baseline) Run Template
```
Execute this task WITHOUT loading any skill:

- Task prompt: "{PROMPT}"
- Input files to copy into working directory:
{FILES_LIST}
- Save all outputs to: {OUTPUT_DIR}
- On completion, save timing.json:
  {
    "total_tokens": {TOKEN_COUNT_FROM_AGENT},
    "duration_ms": {DURATION_MS_FROM_AGENT}
  }

Rules:
- Do not load any external skill or instruction file.
- Work only from the task prompt.
- Copy input files before starting.
- Write all produced files into the output directory.
- Do not modify input files in place. Work on copies.
```

## Assertion Grading Template
```
Grade these outputs against the assertions below.

Output directory: {OUTPUT_DIR}
Task prompt was: "{PROMPT}""

Assertions to check:
{ASSERTIONS_LIST}

Rules:
- Check each assertion independently.
- Require concrete evidence for PASS. Quote the output or cite a file.
- Label FAIL if the label matches but substance is missing.
- Output grading.json:
  {
    "assertion_results": [
      {
        "text": "<assertion>",
        "passed": true|false,
        "evidence": "<concrete evidence from outputs>"
      }
    ],
    "summary": {
      "passed": N,
      "failed": N,
      "total": N,
      "pass_rate": 0.00
    }
  }
```

## Blind Comparison Template
```
Compare these two outputs for the same task. You do not know which came from which configuration.

Task prompt: "{PROMPT}"
Output A directory: {OUTPUT_A_DIR}
Output B directory: {OUTPUT_B_DIR}

Score each on:
- Organization and structure
- Formatting and readability
- Completeness vs. expected output
- Overall polish and usefulness

Output comparison.json:
  {
    "winner": "A" | "B" | "tie",
    "scores": {
      "A": { organization: 1-5, formatting: 1-5, completeness: 1-5, polish: 1-5 },
      "B": { organization: 1-5, formatting: 1-5, completeness: 1-5, polish: 1-5 }
    },
    "reasoning": "<one paragraph>"
  }
```
