# Rubber Duck 🦆

Quick reference for routing and handoffs for a suite of development skills that walk and quack like a duck.

## Topology

- Router: `agents/rubber-duck.agent.md` (picker name `🦆`)
- Ducklings:
  - `agents/duck-investigator.agent.md`
  - `agents/duck-reviewer.agent.md`
  - `agents/duck-adversary.agent.md`
  - `agents/duck-simple.agent.md`
  - `agents/duck-dry.agent.md`
  - `agents/duck-builder.agent.md`
- Skills:
  - `src/skills/rubber-duck/duck-explain/SKILL.md`
  - `src/skills/rubber-duck/duck-debug/SKILL.md`
  - `src/skills/rubber-duck/duck-design/SKILL.md`
  - `src/skills/rubber-duck/duck-review/SKILL.md`
  - `src/skills/rubber-duck/duck-teach/SKILL.md`
  - `src/skills/rubber-duck/duck-triage/SKILL.md`

## Router quick map

- Review input (diff/code): start `duck-review`; chain `duck-reviewer` + `duck-adversary` + `duck-simple` (+`duck-dry` on duplication signal; `duck-triage` on test-gap signal).
- Debug input (code + complaint): start `duck-debug`; chain `duck-investigator`; escalate `duck-triage` if repro weak; use `duck-builder` only for explicit bounded patch requests.
- Explain input (snippet/path/log): start `duck-explain`; hand off to `duck-debug` for root-cause hunt, or `duck-review` for review output.
- Design/tradeoff: start `duck-design`; chain `duck-simple` + `duck-adversary` (+`duck-dry` when shared-rule duplication appears).
- Teach/how-it-works: `duck-teach`; hand off to `duck-debug` or `duck-review` if issue/review request emerges.
- Test planning/coverage: `duck-triage`; chain `duck-review` when inline PR comments are needed.
- Unrecognized: ask one clarifying question, then route.

## Duckling roles (purpose + handoff)

- `duck-investigator`: evidence collection only (defs/refs/callers/tests/imports). Hands implementation work to `duck-builder`.
- `duck-reviewer`: final review comment stream. Delegates review contract to `duck-review`.
- `duck-adversary`: failure/rollback/compat/security-misuse lens. Hands formatting and final thread output to `duck-reviewer`.
- `duck-simple`: complexity minimization lens. Hands final review thread output to `duck-reviewer`.
- `duck-dry`: duplication/divergence lens. Hands final review thread output to `duck-reviewer`.
- `duck-builder`: bounded patching (1–2 files) after upstream diagnosis/review decision.

For exact prefixes/output rules, see each agent file directly.

## Skill roles (purpose + handoff)

- `duck-explain`: fast interpretation of code/log/query/config using short What/Why/Watch out/Next question blocks. Handoff to `duck-debug`, `duck-design`, `duck-review`, `duck-triage`, or `duck-teach` as needed.
- `duck-debug`: Socratic runtime debugging. Handoff to `duck-triage` when repro remains weak.
- `duck-design`: tradeoff and architecture facilitation. Handoff to `duck-debug` for runtime-value issues.
- `duck-review`: review workflow + output contract source of truth. Used by `duck-reviewer`.
- `duck-teach`: structured tutorial generation. Handoff to `duck-debug` or `duck-review` when needed.
- `duck-triage`: test-gap and severity triage. Handoff inline review comments to `duck-review`.

## Related docs

- `agents/README.md`
- `src/skills/rubber-duck/duck-review/references/review-comment-examples.md`

Promoted install artifacts are generated under `skills/rubber-duck/**` via `npm run build:skills`.
