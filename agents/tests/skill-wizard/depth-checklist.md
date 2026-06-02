# Skill Wizard Depth Selection - Manual Test Checklist

Validates State 0.5 behavior in `agents/skill-wizard.agent.md`:

- recommend depth when signals clearly skew (quick vs deep)
- fallback to neutral question when signals are mixed
- honor explicit user depth request
- allow user override of recommendation
- skip depth selection on resume path (`completed: false` plan)

## Test assets

- Runsheet generator: `agents/tests/skill-wizard/generate-depth-runsheet.py`
- Resume fixture: `agents/tests/skill-wizard/fixtures/resume-incomplete.skill-plan.yaml`

## Preflight

- [ ] Use fresh session per scenario unless scenario says otherwise.
- [ ] Capture first assistant response verbatim.
- [ ] Record whether first response contains exactly one question.
- [ ] For recommendation scenarios, confirm override path remains explicit.

## Generate a run sheet

```bash
python3 agents/tests/skill-wizard/generate-depth-runsheet.py
```

Optional custom output path:

```bash
python3 agents/tests/skill-wizard/generate-depth-runsheet.py --output /tmp/skill-wizard-runsheet.md
```

## Manual execution protocol

1. Open generated run sheet.
2. Run scenarios in order.
3. For each scenario:
   - send the exact prompt shown
   - copy first assistant response into the run sheet
   - mark pass/fail against expected first prompt behavior
4. For `SW-D05`, send second message `deep` after recommendation and capture next response.
5. For `SW-D06`, prepare working directory:
   - copy fixture to working dir as `.skill-plan.yaml`
   - run scenario in that directory

## Pass criteria

- Required pass: `SW-D01`..`SW-D06` all pass.
- Blocking failures:
  - wrong recommendation direction on clear-signal scenarios
  - missing neutral fallback on ambiguous scenario
  - explicit depth not honored
  - no override path after recommendation
  - resume scenario asks depth question instead of resuming
  - first response contains multiple stacked questions

## Failure triage

- If only wording mismatch but behavior correct: treat as warn and update expected string in runsheet template.
- If behavior mismatch: open issue against `agents/skill-wizard.agent.md` with:
  - scenario ID
  - exact prompt
  - observed first response
  - expected response pattern
