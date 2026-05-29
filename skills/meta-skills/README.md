# Meta-Skills

A tool kit for agent skills development lifecycle.

Toolkit comprises of:
- skill-plan: For deep skill design and discovery
- skill-forge: Generation & scaffolding skill before creation based off the skill-plan or invoked directly
- skill-doc: Produces skill documentation
- skill-check: Skill audit & linter against the agentskills.io spec, produces a report that can be passed to skill-refine
- skill-eval: Test creation and running framework, produces a report that can be passed to skill-refine
- skill-refine: For iterative updates from the user input or provided from reports.

```
       [ User Intent ]
              │
              ▼
      [  skill-plan  ] ──────(Interrogation & Discovery)
              │
              ▼
      ┌───────────────┐
      │ skill-plan.yaml ◄────────────────────────────────────────┐
      └───────┬───────┘                                          │
              │                                                  │ (Iterative Updates)
              ├───(Optional: Direct Entry)                       │
              ▼                                                  │
      [  skill-forge ] ──────(Generates / Scaffolds)             │
              │                                                  │
              ▼                                                  │
      ┌───────────────┐                                          │
      │ Skill Bundle  │ ◄──────────┐                             │
      └───────┬───────┘            │                             │
              │                    │ (Applies Code Changes)      │
              ├────────────────────┼───────────────┐             │
              ▼                    ▼               ▼             │
      [  skill-doc   ]      [ skill-check ] [  skill-eval ]      │
              │                    │               │             │
              ▼                    ▼               ▼             │
      ┌───────────────┐     ┌──────────────┐┌──────────────┐     │
      │ Documentation │     │ check-report ││  eval-logs   │     │
      └───────────────┘     └──────┬───────┘└──────┬───────┘     │
                                   │               │             │
                                   └───────┬───────┘             │
                                           ▼                     │
                                    [ skill-refine ] ────────────┘
                                           │
                                           └─(Triggers post-fix)─► [ skill-doc ]
```