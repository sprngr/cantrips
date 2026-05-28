# Evaluation Workspace Layout
## Purpose
Reference diagram for the eval workspace directory structure. Read before scaffolding or debugging run paths.

## Structure
```
<skill-name>-workspace/
├── skill-snapshot/               # cp -r of skill before eval iteration
│   ├── SKILL.md
│   └── ...
├── iteration-1/
│   ├── benchmark.json
│   ├── eval-report.html
│   ├── eval-<slug>-1/
│   │   ├── with_skill/
│   │   │   ├── outputs/          # files produced by the run
│   │   │   ├── timing.json
│   │   │   └── grading.json
│   │   └── without_skill/
│   │       ├── outputs/
│   │       ├── timing.json
│   │       └── grading.json
│   ├── eval-<slug>-2/
│   │   └── ...
│   └── eval-<slug>-3/
│       └── ...
├── iteration-2/
│   └── ...
└── feedback.json                 # human review notes per eval
```

## Rules
- One iteration directory per eval loop pass. Number sequentially.
- Each eval gets its own directory named `eval-<slug>-<id>`.
- `with_skill` runs against the snapshot. `without_skill` runs with no skill.
- When improving an existing skill, use snapshot as baseline. Replace `without_skill/` with `old_skill/` if comparing to previous version only.
- All JSON artifacts (`timing.json`, `grading.json`, `benchmark.json`) live alongside `outputs/`, not inside it.
- `feedback.json` is per-iteration, not per-eval. One file aggregates human comments.
