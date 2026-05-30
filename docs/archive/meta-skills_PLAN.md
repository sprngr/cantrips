# Meta-Skills Toolkit — Refinement Plan

Status: Implemented (Steps 1-4 complete)
Date: 2026-05-29

## Context

skill-plan and skill-wizard agent have been deployed. Before continuing buildout, the toolkit design was revisited to enforce single-responsibility per tool and eliminate overlap.

## Decisions Made

### 1. Drop skill-doc

**Rationale:** Solves a problem not yet encountered. The pipeline has natural seams — skill-doc can be added later if needed without disrupting existing tools.

### 2. skill-forge becomes a pure generator

**Current state:** skill-forge has its own interview process and can be invoked directly or from a plan yaml.

**Change:** Strip interview logic from skill-forge. It becomes a pure code generator: `.skill-plan.yaml` in, skill bundle out. Validation at draft time is retained.

**Rationale:** skill-wizard + skill-plan own all interrogation. Having forge also interview creates overlap and deviation risk. Single entry point for discovery, single tool for generation.

### 3. skill-wizard absorbs tiered interview

**Change:** skill-wizard gains the ability to detect skill complexity and tier its interrogation depth. Simple skills get a short interview (3-4 questions). Complex skills (multi-role, pipeline, hybrid) get full interrogation via skill-plan.

**Rationale:** Preserves the quick-skill path that forge's direct invocation currently serves, but routes it through the canonical entry point.

### 4. skill-refine outputs plan yaml patches

**Change:** skill-refine's output is a patch to the existing `.skill-plan.yaml`, not direct code changes or a fresh directive.

**Rationale:** Plan yaml is the single source of truth. Refine patches it, forge rebuilds from it. Clean data flow, no ambiguity about what changed.

### 5. Human-in-the-loop refinement cycle

**Decision:** No automated orchestration of the check → refine → rebuild loop. Human decides which reports to feed, when to refine, when to rebuild.

**Rationale:** Keeps tools simple. Orchestration can be layered on later if the manual loop proves tedious.

## Implementation Status

1. ✅ **Strip skill-forge interview logic** — yaml-in, bundle-out only
2. ✅ **Update skill-wizard** — tiered interview (simple + complex paths)
3. ✅ **Promote skill-refine** — deployed under `.agents/skills/skill-refine`
4. ✅ **Remove skill-doc references** — documentation aligned to 5-tool toolkit

## Final Toolkit

| Tool | Single Responsibility |
|---|---|
| skill-wizard (agent) | Tiered interrogation |
| skill-plan | Decision capture → `.skill-plan.yaml` |
| skill-forge | Generate + validate from yaml |
| skill-check | Audit against spec → report |
| skill-eval | Test & benchmark → logs |
| skill-refine | Patch yaml from reports/user input |
