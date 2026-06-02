# NLTK setup for `scripts/strip-filler.sh`

`scripts/strip-filler.sh` uses NLTK POS tagging for filler removal.
Script auto-installs NLTK package and required tagger data if missing.
Script retries install once. Script fails if both attempts fail.

## Auto-install flow

On run, script executes:

```bash
python -m pip install --upgrade nltk
python -m nltk.downloader averaged_perceptron_tagger_eng averaged_perceptron_tagger
```

Script runs commands in active venv/site.

## Manual install fallback

```bash
python -m pip install --upgrade nltk
python -m nltk.downloader averaged_perceptron_tagger_eng averaged_perceptron_tagger
```

## Verify

```bash
python - <<'PY'
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize
print(pos_tag(wordpunct_tokenize("really quick check")))
PY
```

If verify fails, rerun manual install commands.

## Run self-tests

```bash
bash scripts/tests/run-tests.sh
```

Tests hard-fail if auto-install cannot provision NLTK.
