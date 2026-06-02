#!/usr/bin/env bash
set -euo pipefail

if [[ $# -gt 1 ]]; then
  printf 'Usage: %s [input-file]\n' "$0" >&2
  exit 64
fi

python_bin="${PYTHON_BIN:-}"
if [[ -z "$python_bin" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    python_bin="python3"
  elif command -v python >/dev/null 2>&1; then
    python_bin="python"
  else
    printf 'Error: python runtime not found. Install python3.\n' >&2
    exit 2
  fi
fi

nltk_ready() {
  "$python_bin" - <<'PY' >/dev/null 2>&1
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize

pos_tag(wordpunct_tokenize("really quick check"))
PY
}

install_nltk_stack() {
  "$python_bin" -m pip install --upgrade nltk
  "$python_bin" -m nltk.downloader averaged_perceptron_tagger_eng averaged_perceptron_tagger
}

ready=0
for attempt in 1 2; do
  if nltk_ready; then
    ready=1
    break
  fi

  printf 'NLTK missing/incomplete. Installing (attempt %s/2).\n' "$attempt" >&2
  if ! install_nltk_stack >&2; then
    printf 'NLTK install attempt %s failed.\n' "$attempt" >&2
  fi
done

if [[ "$ready" -ne 1 ]] && ! nltk_ready; then
  printf 'Error: unable to provision NLTK after 2 attempts.\n' >&2
  printf 'Run: %s -m pip install --upgrade nltk\n' "$python_bin" >&2
  printf 'Run: %s -m nltk.downloader averaged_perceptron_tagger_eng averaged_perceptron_tagger\n' "$python_bin" >&2
  exit 3
fi

py_tmp="$(mktemp)"
trap 'rm -f "$py_tmp"' EXIT

cat > "$py_tmp" <<'PY'
import re
import sys
from pathlib import Path

try:
    from nltk import pos_tag
    from nltk.tokenize import wordpunct_tokenize
    from nltk.tokenize.treebank import TreebankWordDetokenizer
except ImportError:
    print("Error: NLTK unavailable after bootstrap.", file=sys.stderr)
    print("Run: python -m pip install --upgrade nltk", file=sys.stderr)
    sys.exit(3)

if len(sys.argv) == 2:
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
else:
    text = sys.stdin.read()

single_fillers = {"just", "really", "basically", "actually", "literally"}
single_filler_tags = {"RB", "RBR", "RBS", "UH"}
phrase_heads = {"kind", "sort"}
phrase_head_tags = {"NN", "JJ", "RB", "RBR", "RBS"}

url_re = re.compile(r"https?://[^\s`]+")
abs_path_re = re.compile(r"/(?:[A-Za-z0-9_.-]+)(?:/[A-Za-z0-9_.-]+)*(?:\.[A-Za-z0-9_.-]+)?")
rel_path_re = re.compile(r"(?<![:\w])(?:\./|\.\./)?[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+")
hyphen_compound_re = re.compile(r"\b[A-Za-z0-9]+(?:[._][A-Za-z0-9]+)*(?:-[A-Za-z0-9]+(?:[._][A-Za-z0-9]+)*)+\b")
code_span_re = re.compile(r"(`[^`]*`)")

detok = TreebankWordDetokenizer()
out_lines = []
in_fence = False


def mask_pattern(segment, pattern, placeholders, counter):
    def replace(match):
        token = f"PROTECTEDTOKEN{counter[0]}X"
        counter[0] += 1
        placeholders[token] = match.group(0)
        return token

    return pattern.sub(replace, segment)


def mask_protected(segment):
    placeholders = {}
    counter = [0]

    segment = mask_pattern(segment, url_re, placeholders, counter)
    segment = mask_pattern(segment, abs_path_re, placeholders, counter)
    segment = mask_pattern(segment, rel_path_re, placeholders, counter)
    segment = mask_pattern(segment, hyphen_compound_re, placeholders, counter)
    return segment, placeholders


def unmask_protected(segment, placeholders):
    for token, original in placeholders.items():
        segment = segment.replace(token, original)
    return segment

def filter_tokens(tagged_tokens):
    kept = []
    i = 0
    while i < len(tagged_tokens):
        token, tag = tagged_tokens[i]
        lower = token.lower()

        if i + 1 < len(tagged_tokens):
            nxt_token, nxt_tag = tagged_tokens[i + 1]
            if (
                lower in phrase_heads
                and nxt_token.lower() == "of"
                and tag in phrase_head_tags
                and nxt_tag == "IN"
            ):
                i += 2
                continue

        if lower in single_fillers and tag in single_filler_tags:
            i += 1
            continue

        kept.append(token)
        i += 1

    return kept


def process_plain_segment(segment):
    match = re.match(r"^(\s*)(.*?)(\s*)$", segment, flags=re.DOTALL)
    leading, body, trailing = match.groups()
    if not body:
        return segment

    masked, placeholders = mask_protected(body)
    tokens = wordpunct_tokenize(masked)
    if not tokens:
        return segment

    tagged = pos_tag(tokens)
    filtered = filter_tokens(tagged)
    cleaned = detok.detokenize(filtered) if filtered else ""
    restored = unmask_protected(cleaned, placeholders)
    return f"{leading}{restored}{trailing}"


def process_core(core):
    parts = code_span_re.split(core)
    output_parts = []

    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            output_parts.append(part)
            continue

        output_parts.append(process_plain_segment(part))

    return "".join(output_parts)

try:
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            out_lines.append(line)
            in_fence = not in_fence
            continue

        if in_fence:
            out_lines.append(line)
            continue

        if not line.strip():
            out_lines.append("")
            continue

        match = re.match(r"^(\s*)(.*?)(\s*)$", line)
        prefix, core, _suffix = match.groups()

        cleaned = process_core(core)
        out_lines.append(f"{prefix}{cleaned}")
except LookupError as err:
    print("Error: NLTK model data unavailable after bootstrap.", file=sys.stderr)
    print(
        "Run: python -m nltk.downloader averaged_perceptron_tagger_eng averaged_perceptron_tagger",
        file=sys.stderr,
    )
    print(f"Details: {str(err).splitlines()[0]}", file=sys.stderr)
    sys.exit(3)

text = "\n".join(out_lines)

text = re.sub(r"(?<=\S)[ \t]{2,}(?=\S)", " ", text)
text = re.sub(r"[ \t]+\n", "\n", text)
text = re.sub(r"\n{3,}", "\n\n", text)
print(text.strip())
PY

"$python_bin" "$py_tmp" "$@"
