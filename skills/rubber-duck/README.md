# Rubber Duck 🦆

A suite of development skills that walk and quack like a duck.
Socratic, terse, domain-segregated.

## Agent

- `agents/rubber-duck.agent.md` routes incoming context to the correct skill.
- Unrecognized input: ask 1 clarifying question, then route.

## Skills

| Skill | Role | Trigger |
| --- | --- | --- |
| `duck-debug` | Root-cause tracing; Socratic questioning; execution path tracing; runtime assumptions. | `debug this`, `why broken`, `help me understand` |
| `duck-design` | Architecture facilitation; tradeoff matrices; alternative comparison; system-level assumptions. | `design this`, `tradeoffs`, `evaluate approach` |
| `duck-teach` | Structured tutorials; What -> Why -> Example -> Pitfalls -> See also; depth scales. | `teach me X`, `show me X`, `how does X work` |
| `duck-triage` | Test coverage analysis; bug severity classification; pre-PR planning; edge case discovery. | `test coverage`, `what to test`, `triage this bug` |
| `duck-review` | Code review comments; extends caveman-review; one-line findings; in-PR annotation. | `review this`, `code review`, `review the diff` |

## Domain Separation

### Ownership

| Concern | Owner |
| --- | --- |
| Null/empty/stale runtime values | `duck-debug` |
| Scaling, compat, rollback | `duck-design` |
| Pre-PR `what to test` | `duck-triage` |
| In-PR missing test annotation | `duck-review` |

### Redirect Patterns

| Pattern | Route |
| --- | --- |
| Tutorial reveals bug | `duck-teach` -> `duck-debug` |
| Debug wrapped in design language | `duck-debug` -> `duck-design` |
