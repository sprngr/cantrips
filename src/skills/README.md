# Skills development guide

`src/skills/` is development source of truth.

`skills/` is promoted install artifact generated from `src/skills/**/.release-files`.

`src/skills/experimental/**` is source-only and excluded from promotion. Promoted tree keeps only `skills/experimental/README.md` as pointer note.

## Workflow

1. Create or update skill under `src/skills/<category>/<skill-name>/`.
2. Keep dev-only files in source tree as needed (`scripts/tests`, `.skill-plan.yaml`, drafts).
3. Maintain `.release-files` allowlist in each concrete skill directory.
4. Build + verify promoted output.

```bash
npm run build:skills
npm run check:skills
```

5. Commit both source and promoted output changes.

## `.release-files` template

Example: `src/skills/<category>/<skill-name>/.release-files`

```text
# Required
SKILL.md

# Runtime references/docs
references/

# Runtime scripts
scripts/run-checks.sh

# Optional eval artifact
evals/evals.json

# Exclude dev-only artifacts:
# - .skill-plan.yaml
# - scripts/tests/
# - *.test.* / *.spec.*
```

## Guardrails

- Missing `.release-files` for any concrete skill fails checks.
- Forbidden promoted artifacts fail checks (`tests/`, `.skill-plan*`, test/spec files).
- Experimental skill directories are forbidden in promoted output (`skills/experimental/**`), except `skills/experimental/README.md`.
- Stale promoted output fails checks; rebuild with `npm run build:skills`.
