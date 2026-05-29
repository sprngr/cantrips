# Blind Comparison Prompt
## Purpose
Compare two skill outputs without knowing which came from with-skill or without-skill runs. Eliminates label bias in LLM grading.

## Prompt
Fill variables. Dispatch to a fresh subagent.

```
You are an impartial evaluator. Read both outputs for the same task prompt.

Task: "{PROMPT}"

Output A files: {LIST_FILES_A}
Output B files: {LIST_FILES_B}

Score each dimension 1-5:
- Organization: logical structure, clear sections
- Formatting: readable, consistent, professional
- Completeness: covers all requested work
- Accuracy: claims match evidence in outputs
- Usefulness: practical value to end user

Produce comparison.json:
{
  "winner": "A" | "B" | "tie",
  "scores": {
    "A": { "organization": N, "formatting": N, "completeness": N, "accuracy": N, "usefulness": N },
    "B": { "organization": N, "formatting": N, "completeness": N, "accuracy": N, "usefulness": N }
  },
  "delta": { "organization": N, "formatting": N, "completeness": N, "accuracy": N, "usefulness": N },
  "reasoning": "<specific differences observed>"
}
```

## When to use
Run after assertion grading. Complements pass/fail data with holistic quality scoring. Use when both configurations pass most assertions but differ in polish.
