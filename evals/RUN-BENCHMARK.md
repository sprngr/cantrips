# Rubber Duck Benchmark Manual

How to run baseline vs candidate benchmark for Ponytail-inspired Rubber Duck updates.

This manual has two modes:

- **Quick operator runbook** (copy/paste commands)
- **Full benchmark guide** (setup, scoring, interpretation)

Scope: **local worktree A/B flow only**.

---

## 0) Files used

- Benchmark rubric + tables: `evals/rubber-duck-benchmark.md`
- Case suite: `evals/cases/rubber-duck.json`
- Validator script: `scripts/run-rubber-duck-evals.js`
- Compare script: `scripts/compare-rubber-duck-evals.js`

Optional npm aliases:

- `npm run evals:validate:rduck`
- `npm run evals:compare:rduck`

---

## 1) Quick Operator Runbook

Use this for fast local A/B verification.

### 1.1 Create baseline/candidate worktrees

```bash
# run from primary repo root
git worktree add /tmp/opencode/cantrips-baseline <BASELINE_REF>
git worktree add /tmp/opencode/cantrips-candidate <CANDIDATE_REF>

npm --prefix /tmp/opencode/cantrips-baseline ci
npm --prefix /tmp/opencode/cantrips-candidate ci
```

### 1.2 Validate eval schema in each worktree

```bash
node /tmp/opencode/cantrips-baseline/scripts/run-rubber-duck-evals.js \
  --cases /tmp/opencode/cantrips-baseline/evals/cases/rubber-duck.json \
  --out /tmp/opencode/cantrips-baseline/evals/results/validate.json

node /tmp/opencode/cantrips-candidate/scripts/run-rubber-duck-evals.js \
  --cases /tmp/opencode/cantrips-candidate/evals/cases/rubber-duck.json \
  --out /tmp/opencode/cantrips-candidate/evals/results/validate.json
```

### 1.3 Compare baseline vs candidate reports

```bash
node scripts/compare-rubber-duck-evals.js \
  --baseline /tmp/opencode/cantrips-baseline/evals/results/validate.json \
  --candidate /tmp/opencode/cantrips-candidate/evals/results/validate.json \
  --out evals/results/ab-compare.json \
  --summary evals/results/ab-compare.md
```

### 1.4 Read outputs

- Machine report: `evals/results/ab-compare.json`
- Human summary: `evals/results/ab-compare.md`

If schema validation fails, fix case JSON first.

---

## 2) Full Benchmark Guide

## 2.1 Benchmark objective

Confirm candidate improves behavior while preserving safety:

- routing accuracy
- contract compliance
- safety correctness
- root-cause quality
- patch discipline
- review signal quality
- efficiency

Use weighted scoring in `evals/rubber-duck-benchmark.md`.

---

## 2.2 Prepare A/B environment

1. Pick refs:
   - baseline: pre-update commit/branch
   - candidate: updated branch
2. Create worktrees in `/tmp/opencode/`.
3. Install dependencies in both.
4. Record refs/date in benchmark file section "Branches / Worktrees".

Recommended:

```bash
git -C /mnt/f/workspace/cantrips rev-parse --short <BASELINE_REF>
git -C /mnt/f/workspace/cantrips rev-parse --short <CANDIDATE_REF>
```

---

## 2.3 Lock run conditions

Keep fixed across A/B:

- model
- temperature
- max output tokens
- permissions/tool profile
- retry policy

Record values in benchmark file section "Controlled Run Settings".

---

## 2.4 Run evaluator pipeline

Current scripts provide:

1. **Schema validation** (`run-rubber-duck-evals.js`)
2. **A/B compare reporting** (`compare-rubber-duck-evals.js`)

Note: scoring fields are optional/forward-compatible. If future runners emit scores under `summary.*_score` and `summary.weighted_total`, compare script will include them automatically.

---

## 2.5 Fill weighted score tables (manual process)

Use `evals/rubber-duck-benchmark.md` sections:

- `8) Results Tables`
- `9) Regression Tracker`
- `10) Ship Gate`

### Step-by-step

1. For each case and each run (`n=3` recommended), assign raw score per category:
   - 0 = failed
   - 1 = partial
   - 2 = correct/complete
2. Compute per-category raw mean for baseline and candidate.
3. Convert to weighted score:

```text
weighted_category_score = (mean_raw_score / 2.0) * weight
```

4. Sum all weighted category scores:

```text
weighted_total = Σ weighted_category_score
```

5. Fill:
   - overall weighted table
   - category breakdown table
   - efficiency summary table
6. Log candidate losses in regression tracker.

---

## 2.6 Contract assertion checks (recommended)

Use regex checks from benchmark file section `6) Contract Assertions`.

Minimum checks:

- investigator has evidence IDs and coverage/shared-path lines
- adversary findings include `Impact:` and `Rollback:`
- dry findings include `Diverges when:` and `Extract start:`
- builder output has `verification:` + `evidence:` and honest done/unverified status

These reduce scorer drift.

---

## 2.7 Ship decision

Apply gates from benchmark file section `10) Ship Gate`:

1. safety non-regression
2. weighted total improvement
3. zero critical contract regressions
4. no major routing regression

Mark final checkbox:

- [ ] Ship
- [ ] Iterate and re-run

---

## 3) Common Issues + Fixes

### Issue: compare report shows no scored fields

Cause: current validator outputs schema-only summary.

Fix: expected for now. Fill weighted tables manually until scoring runner exists.

### Issue: validator fails with JSON escape error

Cause: invalid regex escape in case JSON.

Fix:

```bash
python3 -m json.tool evals/cases/rubber-duck.json
```

Then correct escaping and re-run validator.

### Issue: category counts differ between baseline and candidate

Cause: case file drift between worktrees.

Fix: ensure same `evals/cases/rubber-duck.json` content in both refs, or intentionally track the difference in notes.

---

## 4) Recommended command set (copy/paste)

```bash
# 1) A/B setup
git worktree add /tmp/opencode/cantrips-baseline <BASELINE_REF>
git worktree add /tmp/opencode/cantrips-candidate <CANDIDATE_REF>
npm --prefix /tmp/opencode/cantrips-baseline ci
npm --prefix /tmp/opencode/cantrips-candidate ci

# 2) Validate both
node /tmp/opencode/cantrips-baseline/scripts/run-rubber-duck-evals.js --cases /tmp/opencode/cantrips-baseline/evals/cases/rubber-duck.json --out /tmp/opencode/cantrips-baseline/evals/results/validate.json
node /tmp/opencode/cantrips-candidate/scripts/run-rubber-duck-evals.js --cases /tmp/opencode/cantrips-candidate/evals/cases/rubber-duck.json --out /tmp/opencode/cantrips-candidate/evals/results/validate.json

# 3) Compare into current repo
node scripts/compare-rubber-duck-evals.js --baseline /tmp/opencode/cantrips-baseline/evals/results/validate.json --candidate /tmp/opencode/cantrips-candidate/evals/results/validate.json --out evals/results/ab-compare.json --summary evals/results/ab-compare.md
```

---

## 5) Next maturity step (optional)

Implement a scored eval runner that writes:

- `summary.weighted_total`
- `summary.safety_score`
- category scores (`routing`, `contract`, `root_cause`, `patch_discipline`, `review_signal`, `efficiency`)

Then compare script will auto-populate scored-field delta table without manual patching.
