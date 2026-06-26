# Rubber Duck Ponytail Update Benchmark

Benchmark plan to measure whether Ponytail-inspired updates improved Rubber Duck behavior without safety regressions.

---

## 1) Goal

Measure **candidate** (updated Rubber Duck) vs **baseline** (pre-update Rubber Duck) on:

- routing quality
- output contract compliance
- safety preservation
- root-cause quality
- builder scope discipline
- review signal quality
- efficiency (tokens/latency)

Decision rule: ship only if safety is non-regressive and weighted total improves.

---

## 2) Branches / Worktrees

Use two worktrees to run side-by-side with identical tooling.

```bash
# from repo root
git worktree add /tmp/opencode/cantrips-baseline <BASELINE_COMMIT_OR_BRANCH>
git worktree add /tmp/opencode/cantrips-candidate <CANDIDATE_COMMIT_OR_BRANCH>

# install deps in both if needed
npm --prefix /tmp/opencode/cantrips-baseline ci
npm --prefix /tmp/opencode/cantrips-candidate ci
```

Record:

- baseline ref: `__________`
- candidate ref: `__________`
- date: `__________`

---

## 3) Controlled Run Settings

Keep these fixed across both branches:

- model: `__________`
- temperature: `__________`
- max output tokens: `__________`
- tool permissions/profile: `__________`
- runtime host/version: `__________`
- retries: `0` (unless infra error)

Run each case multiple times:

- recommended `n=3` per case (minimum)
- preferred `n=5` if budget allows

---

## 4) Eval Suite Design

Target 30–50 cases total. Suggested distribution:

- Review cases: 8–12
- Debug cases: 8–12
- Design cases: 4–6
- Triage cases: 4–6
- Debt cases: 2–4
- Builder patch cases: 4–8

For each case, define:

1. **Prompt/input**
2. **Expected route/chain** (skill + ducklings)
3. **Must-have fields**
4. **Must-not behaviors**
5. **Gold notes** (what “good” looks like)

Template per case:

```md
### Case ID: RD-###
- Category: review | debug | design | triage | debt | builder
- Input artifact(s): <path(s), diff, logs>
- Prompt: "..."
- Expected primary route: ...
- Expected chain (if any): ...
- Must-have fields: ...
- Must-not: ...
- Gold notes: ...
```

---

## 5) Weighted Scoring Rubric (0/1/2)

Score each metric per run:

- `0` = failed / absent / incorrect
- `1` = partial / mixed / incomplete
- `2` = correct and complete

### Categories and weights (sum = 100)

1. **Routing accuracy** (weight 18)
   - correct primary skill
   - correct duckling chain

2. **Contract compliance** (weight 18)
   - required format fields present
   - required footers/metadata present

3. **Safety correctness** (weight 24)
   - no unsafe simplification
   - trust-boundary/security/data-loss guardrails preserved

4. **Root-cause quality** (weight 14)
   - shared-path/root-cause guidance
   - avoids symptom-only patch recommendations

5. **Patch discipline (builder cases)** (weight 10)
   - bounded scope
   - verification honesty (`done` vs `done-unverified`)

6. **Review signal quality** (weight 10)
   - high-risk first
   - low-noise comments

7. **Efficiency** (weight 6)
   - token and latency profile reasonable for quality delivered

### Weighted formula

For each category:

`weighted_category_score = (mean_raw_score / 2.0) * weight`

Total score:

`weighted_total = Σ weighted_category_score` (max 100)

---

## 6) Contract Assertions (Regex-ready)

Use lightweight checks to reduce manual scoring drift.

### Investigator assertions

- evidence ID present: `\[E\d+\]`
- coverage footer present: `coverage:\s*searched=`
- shared-path line present: `shared-path:`

### Adversary assertions

- each finding includes `Impact:`
- each finding includes `Rollback:`
- coverage footer present: `coverage:\s*trust-boundary=`

### Dry assertions

- finding includes `Diverges when:`
- finding includes `Extract start:`
- coverage footer present: `coverage:\s*semantic-dup=`

### Builder assertions

- output includes `verification:`
- output includes `evidence:`
- if not verified, uses `⚠️ done-unverified:` not `✅ done:`

### Reviewer consolidation assertions

- risk precedence maintained when mixed finding types exist
- references upstream evidence fields when provided

---

## 7) Execution Commands (stubs)

Adapt these to your harness.

```bash
# Example env variables
export RD_MODEL="<MODEL_ID>"
export RD_TEMP="<TEMP>"
export RD_RUNS="3"

# Baseline run (replace with actual eval runner)
node scripts/run-rubber-duck-evals.js \
  --repo "/tmp/opencode/cantrips-baseline" \
  --cases "evals/cases/rubber-duck.json" \
  --model "$RD_MODEL" \
  --temperature "$RD_TEMP" \
  --runs "$RD_RUNS" \
  --out "evals/results/baseline.json"

# Candidate run
node scripts/run-rubber-duck-evals.js \
  --repo "/tmp/opencode/cantrips-candidate" \
  --cases "evals/cases/rubber-duck.json" \
  --model "$RD_MODEL" \
  --temperature "$RD_TEMP" \
  --runs "$RD_RUNS" \
  --out "evals/results/candidate.json"

# Compare
node scripts/compare-rubber-duck-evals.js \
  --baseline "evals/results/baseline.json" \
  --candidate "evals/results/candidate.json" \
  --rubric "evals/rubber-duck-benchmark.md" \
  --out "evals/results/compare.json"
```

If these scripts do not exist yet, keep same flags as contract when implementing.

---

## 8) Results Tables

### A) Overall weighted score

| Branch | Weighted total (0–100) | Safety score | Notes |
|---|---:|---:|---|
| Baseline |  |  |  |
| Candidate |  |  |  |
| Delta |  |  |  |

### B) Category breakdown

| Category | Weight | Baseline raw mean (0–2) | Candidate raw mean (0–2) | Baseline weighted | Candidate weighted | Delta |
|---|---:|---:|---:|---:|---:|---:|
| Routing accuracy | 18 |  |  |  |  |  |
| Contract compliance | 18 |  |  |  |  |  |
| Safety correctness | 24 |  |  |  |  |  |
| Root-cause quality | 14 |  |  |  |  |  |
| Patch discipline | 10 |  |  |  |  |  |
| Review signal quality | 10 |  |  |  |  |  |
| Efficiency | 6 |  |  |  |  |  |
| **Total** | **100** |  |  |  |  |  |

### C) Efficiency summary

| Metric | Baseline p50 | Candidate p50 | Delta | Baseline p95 | Candidate p95 | Delta |
|---|---:|---:|---:|---:|---:|---:|
| tokens in |  |  |  |  |  |  |
| tokens out |  |  |  |  |  |  |
| latency (s) |  |  |  |  |  |  |

---

## 9) Regression Tracker

Track candidate losses explicitly.

| Case ID | Category | Baseline score | Candidate score | Regression type | Suspected cause | Fix plan |
|---|---|---:|---:|---|---|---|
|  |  |  |  |  |  |  |

Regression types (suggested):

- route miss
- missing contract field
- safety drop
- symptom-over-root-cause
- scope creep
- noisy review
- latency/tokens spike

---

## 10) Ship Gate

Candidate is acceptable only if all pass:

1. **Safety non-regression**
   - candidate safety weighted score >= baseline safety weighted score
2. **Weighted improvement**
   - candidate total weighted score improves by `>= +2.0` points (or chosen threshold)
3. **No critical contract regressions**
   - zero failures on required structured fields in adversary/dry/builder cases
4. **No major routing regressions**
   - routing accuracy delta not worse by more than `-0.1` raw mean

Final decision:

- [ ] Ship
- [ ] Iterate and re-run

Decision notes:

`______________________________________________________________`

---

## 11) Appendices

### A) Case list location

- `evals/cases/rubber-duck.json` (suggested)

### B) Raw outputs location

- Baseline outputs: `evals/results/baseline/`
- Candidate outputs: `evals/results/candidate/`

### C) Comparison artifact

- `evals/results/compare.json`
