---
name: squash
description: Compresses session context into ultra-compact AI handoff text without meaning loss. Use when user asks to squash/compress context for AI handoff or token reduction.
---

Compress session context for handoff. Keep meaning. Cut tokens.

## When to use

- Use when user asks "squash", "compress context", or "handoff summary".
- Use when target output path is known.
- Skip when user requests full narrative transcript.

## Instructions/Workflows

1. Define scope boundary from user request. Output: one line `scope: ...`.
2. Generate compact handoff from source context with full-path file references. Output: markdown with `Goal`, `Decisions`, `Open questions`, `Next actions`.
3. Rewrite compact handoff in caveman-terse style. Output: terse markdown.
4. Resolve output mode from user input. Output: one line `target_path: <path|auto-temp>`.
5. Call `Bash scripts/squash-session.sh [target-path] [input-file]` with step-3 text on stdin. Output: one line `saved: <path>` on stdout.
6. Report final handoff and saved path to user. Output: terse markdown plus `saved:` line.

## Handoff document rules

1. Treat user arguments as next-session focus when arguments exist. Output: one line `focus: ...`.
2. Add section `Suggested skills` with skill names and one-line reason per skill.
3. Reference existing PRDs, plans, ADRs, issues, commits, and diffs by path or URL.
4. Redact API keys, passwords, tokens, and personally identifiable information.
5. Skip duplication of content already captured in referenced artifacts.
6. Keep output summary concise for fresh-agent continuation.

## References

- See [Example.md](references/Example.md)
- See [NLTK-Setup.md](references/NLTK-Setup.md)
- Run `bash scripts/tests/run-tests.sh` to validate `scripts/strip-filler.sh`.
- See [squash-session.sh](scripts/squash-session.sh)
- See [strip-filler.sh](scripts/strip-filler.sh)
- See [write-handoff.sh](scripts/write-handoff.sh)
