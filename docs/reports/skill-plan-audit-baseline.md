# Skill Plan Audit Baseline

- **Date:** 2026-05-30
- **Task:** ADR-0002 Task 1 (baseline inventory and violation report)
- **Scope:** tracked `**/.skill-plan.yaml` files
- **Total files audited:** 6

## Rule Set Used

From ADR-0002 strict write contract:
- `target_path` is relative, starts with `skills/`, ends with `/`, no `..`, no leading `/`
- enum fields constrained (`scope`, `mechanism`, `context_assets`, `tier`, `example_placed`)
- `workflow_notes` must be list of strings
- `coverage.essential_schema` complete boolean set
- `coverage.unanswered_branches` must be array

## Violation Summary

| Violation | Count |
|---|---:|
| `target_path_abs` | 3 |
| `target_path_not_skills_prefix` | 3 |
| `target_path_no_trailing_slash` | 1 |
| `enum_context_assets` | 3 |
| `workflow_notes_not_list_of_strings` | 1 |
| `coverage_missing` | 2 |
| all other tracked violations | 0 |

## File-by-File Results

| File | `target_path` | `context_assets` | `workflow_notes` type | Violations |
|---|---|---|---|---|
| `skills/goblin-mode/.skill-plan.yaml` | `skills/goblin-mode/` | `none` | `list` | none |
| `skills/meta-skills/skill-check/.skill-plan.yaml` | `/mnt/f/workspace/cantrips/skills/skill-check` | `checklists + templates` | `list` | `target_path_abs`, `target_path_not_skills_prefix`, `target_path_no_trailing_slash`, `enum_context_assets`, `coverage_missing` |
| `skills/meta-skills/skill-eval/.skill-plan.yaml` | `/mnt/f/workspace/skills/skill-eval/` | `schemas-in-assets, prompt-templates, checklist, workspace-layout, html-report-template` | `list` | `target_path_abs`, `target_path_not_skills_prefix`, `enum_context_assets`, `coverage_missing` |
| `skills/meta-skills/skill-refine/.skill-plan.yaml` | `/mnt/f/workspace/cantrips/skills/meta-skills/skill-refine/` | `[schema, checklists, templates]` | `dict` | `target_path_abs`, `target_path_not_skills_prefix`, `enum_context_assets`, `workflow_notes_not_list_of_strings` |
| `skills/rubber-duck/duck-review/.skill-plan.yaml` | `skills/rubber-duck/duck-review/` | `templates` | `list` | none |
| `skills/squash/.skill-plan.yaml` | `skills/squash/` | `schema` | `list` | none |

## Initial Migration Targets (for Task 3)

1. Normalize absolute `target_path` values to canonical relative `skills/.../` form.
2. Normalize non-enum `context_assets` using ADR-0002 deterministic rule.
3. Flatten `workflow_notes` object in `skill-refine` to list-of-strings.
4. Restore full `coverage` block in `skill-check` and `skill-eval` plans.

## Notes

- No YAML parse failures.
- No invalid values found for `scope`, `mechanism`, `tier`, `example_placed`.
- Next step: implement strict audit script (`scripts/audit-skill-plans.py`) and rerun as authoritative gate.
