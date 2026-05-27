# Rubber Duck 🦆

A suite of development skills that walk and quack like a duck. Socratic, terse, domain-segregated.

## Skills

| Skill | Role | Trigger |
|---|---|---|
| `duck-debug` | Root-cause tracing. Socratic questioning. Execution path tracing. Runtime assumptions. | "debug this", "why broken", "help me understand" |
| `duck-design` | Architecture facilitation. Tradeoff matrices. Alternative comparison. System-level assumptions. | "design this", "tradeoffs", "evaluate approach" |
| `duck-teach` | Structured tutorials. What → Why → Example → Pitfalls → See also. Depth-scales. | "teach me X", "show me X", "how does X work" |
| `duck-triage` | Test coverage analysis. Bug severity classification. Pre-PR planning. Edge case discovery. | "test coverage", "what to test", "triage this bug" |
| `duck-review` | Code review comments. Extends caveman-review. One-line findings. In-PR annotation. | "review this", "code review", "review the diff" |

## Domain Separation

| Concern | Owner | Redirects to |
|---|---|---|
| Null/empty/stale runtime values | `duck-debug` | — |
| Scaling, compat, rollback | `duck-design` | — |
| Pre-PR "what to test" | `duck-triage` | — |
| In-PR missing test annotation | `duck-review` | — |
| Tutorial reveals bug | → `duck-debug` | — |
| Debug wrapped in design language | → `duck-design` | — |

## Agent

`agents/rubber-duck.agent.md` routes incoming context to the correct skill. Unrecognized input → 1 clarifying question, then route.