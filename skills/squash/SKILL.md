---
name: squash
description: Pack session context into gzip temp payload and restore it in new session with deterministic validation and load instructions. Use when context is large, sessions must be handed off, or token budget is tight.
---
# Squash

Create compact gzip context payloads and restore them safely using goblin mode.

## When to use

- Activate when user asks to compact, hand off, migrate, or restore session context.
- Activate when user needs temporary file output plus exact new-session load steps.

## Instructions/Workflows

1. Run `bash scripts/squash-pack.sh --input "<context-file>"`.
2. Capture JSON keys `payload_path`, `context_sha256`, and `new_session_prompt`.
3. Load `assets/context-envelope.schema.json` before trusting unpacked payload content.
4. Validate envelope keys and constants: `version=1`, `encoding=utf-8`, `algorithm=gzip`.
5. Start new session.
6. Run `bash skills/squash/scripts/squash-unpack.sh --file "<payload_path>"`.
7. Verify first output JSON has `"status":"ok"` and `"sha256_valid":true`.
8. Copy text between `BEGIN_RESTORED_CONTEXT` and `END_RESTORED_CONTEXT`.
9. Paste copied block as first message in new session.
10. Stop load on non-zero exit or any `"status":"error"` JSON.
11. Load `references/restore-playbook.md` when unpack fails schema, hash, or character-count checks.

## Example

### User
Use squash. Pack `/tmp/session.txt`, then tell me exactly how to restore in new session.

### Assistant
Run:
```bash
bash skills/squash/scripts/squash-pack.sh --input "/tmp/session.txt"
```

Capture output JSON keys:
- `payload_path`
- `context_sha256`
- `new_session_prompt`

Before unpack trust, validate envelope contract using:
- `assets/context-envelope.schema.json`

Output example:
```json
{"status":"ok","payload_path":"/tmp/squash-context-a1b2c3.json.gz","context_sha256":"6c0f...","context_chars":18472,"new_session_prompt":"In new session run: bash skills/squash/scripts/squash-unpack.sh --file \"/tmp/squash-context-a1b2c3.json.gz\". Then paste block between BEGIN_RESTORED_CONTEXT and END_RESTORED_CONTEXT as first message."}
```

In new session run:
```bash
bash skills/squash/scripts/squash-unpack.sh --file "/tmp/squash-context-a1b2c3.json.gz"
```

Output starts with metadata JSON:
```json
{"status":"ok","sha256_valid":true,"context_chars":18472}
```

Then output includes:
```text
BEGIN_RESTORED_CONTEXT
...restored context...
END_RESTORED_CONTEXT
```

Paste that block as first message in new session.

### Edge case correction
If unpack output shows:
```json
{"status":"error","code":"sha256_mismatch"}
```
Load `references/restore-playbook.md`.
Re-pack from original source.
Do not load tampered payload.

### Concrete output
Payload created at `/tmp/squash-context-a1b2c3.json.gz`; schema+hash verified; context block ready for first-message bootstrap.

### Agent-calibration notes
- Tone: direct, command-first.
- Pacing: pack → validate → unpack → paste.
- Output shape: preserve script JSON exactly; keep restore block markers unchanged.

## References

- Schema: `assets/context-envelope.schema.json`
- Failure recovery: `references/restore-playbook.md`
