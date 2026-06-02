# Cantrips

🔮 Because I'm still not convinced this isn't magic.

> [!NOTE]
> My preferred harness is [OpenCode](https://opencode.ai/) so you may need to make some tweaks to agents or skill permissions to fit your tooling.

Repository of personal agent skills, helper agents, and skill-authoring playbooks. YMMV. GLHF.

## External Skill Packages

[caveman](https://github.com/JuliusBrussee/caveman): Many of my skills or configs rely on the existence of this for token brevity.

```bash 
npx skills add JuliusBrussee/caveman
```

## Quickstart

Install full repo skill set from a compatible runtime:

```bash
npx skills add sprngr/cantrips --full-depth
```

Or install from local clone while developing:

```bash
npx skills add /path/to/cantrips --full-depth
```

Install included agents (path depends on harness):

```bash
cp /path/to/cantrips/agents/*.agent.md /path/to/harness/agents/
```

## Skill development workflow (`src/skills` -> `skills`)

- `src/skills/` is source of truth for in-development skills.
- Each concrete skill directory must include `.release-files` (allowlist manifest).
- `skills/` is promoted install artifact committed to git for `npx skills add` consumption.
- `src/skills/experimental/**` is excluded from promotion (source-only); `skills/experimental/README.md` remains as pointer note.

Build promoted output:

```bash
npm run build:skills
```

Validate manifests + promoted output guardrails:

```bash
npm run check:skills
```

### New skill checklist

- Create skill under `src/skills/<category>/<skill-name>/`.
- Add required `SKILL.md` and any dev-only files (`scripts/tests`, `.skill-plan.yaml`, drafts) as needed.
- Add `.release-files` in skill root with only files/dirs that should ship.

Example `src/skills/<category>/<skill-name>/.release-files`:

```text
# Required entry
SKILL.md

# Ship references/docs used at runtime
references/

# Ship scripts needed by installed skill
scripts/run-checks.sh

# Optional machine-consumable eval data
evals/evals.json

# Do not include dev-only artifacts (excluded by policy):
# - .skill-plan.yaml
# - scripts/tests/
# - *.test.* / *.spec.*
```

- Run build + checks.

```bash
npm run build:skills
npm run check:skills
```

- Commit both source (`src/skills/**`) and promoted output (`skills/**`).

## Repo map

| Path | Purpose | Details |
| --- | --- | --- |
| `AGENTS.md` | Default prompt added to my sessions | - |
| `agents/` | Routing + specialized agents | [agents/README.md](./agents/README.md) |
| `agents/tests/skill-wizard/` | Manual skill-wizard behavior tests | [agents/tests/skill-wizard/README.md](./agents/tests/skill-wizard/README.md) |
| `src/skills/rubber-duck/` | Rubber-duck workflow skills (development source) | [src/skills/rubber-duck/README.md](./src/skills/rubber-duck/README.md) |
| `src/skills/meta-skills/` | Skill-authoring lifecycle toolkit (development source) | [src/skills/meta-skills/README.md](./src/skills/meta-skills/README.md) |
| `src/skills/experimental/` | Incubating skills (no stability guarantees; development source) | [src/skills/experimental/README.md](./src/skills/experimental/README.md) |
| `skills/` | Promoted install artifacts (built from `src/skills/**/.release-files`) | `npm run build:skills` |

For behavior, triggers, contracts, and workflows, see each subdirectory README.
