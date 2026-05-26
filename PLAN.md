# 🔮 Cantrips — Plan

Because this still feels like magic.

## Vision

Personal repository of agents, skills, and skill playbooks — original creations and curated finds from the web — synced and updated across machines via a lightweight set of scripts that wrap the [`skills`](https://www.npmjs.com/package/skills) npm package.

Open-source-adjacent: MIT licensed. Work for yourself, share for others who want the same toolkit.

## Structure

```
cantrips/
├── PLAN.md              ← living plan, decisions, next steps
├── README.md            ← repo readme (usage)
├── LICENSE              ← MIT
├── AGENTS.md            ← AI persona guidelines
├── .gitattribute        ← normalize line endings (text=auto)
├── agents/              ← agent definitions (*.agent.md), flat
│   └── rubber-duck.agent.md
├── skills/              ← nested skill tree; scripts traverse recursively
│   ├── skill-tree/
│   │   ├── SKILL.md
│   │   └── README.md
│   └── duck-review/
│       ├── SKILL.md
│       └── README.md
├── inventory/           ← machine-readable catalog for the repo
│   ├── catalog.json     ← auto-generated (no registry)
│   └── README.md        ← how to maintain the inventory
├── scripts/             ← tooling
│   ├── skills.sh        ← npx skills CLI wrapper + local skill management
│   ├── catalog.sh       ← rebuild inventory/catalog.json from repo state
│   ├── init.sh          ← one-shot machine setup
│   └── .env             ← configurable defaults (SKILLS_PKG, install_args)
└── archive/             ← unreviewed upstream copies; rename to skills/ after review
```

### Directory semantics

| Directory | Purpose |
|---|-|
| `agents/` | Agent files. Flat. `name.agent.md`. |
| `skills/` | skills are nested. Scripts traverse recursively. |
| `archive/` | Skimmed upstream copies. Not vetted. | Same as `skills/` |
| `inventory/` | Machine-readable catalog (no registry) | `catalog.json` |
| `scripts/` | Bash scripts | `.sh`, POSIX-ish + GNU coreutils |

## Conventions

- **Skill naming**: kebab-case (`skill-tree`, `duck-review`, `modify-memory`)
- **Agent naming**: kebab-case with emoji (`rubber-duck`, `code-architect`)
- **Frontmatter**: `SKILL.md` and `.agent.md` carry `---` frontmatter (`name`, `description`). Descriptions ≤ 1024 chars. Third person. Keyword triggers included.
- **`SKILL.md` hard requirement**: agentskills.io spec. Skills without it are invalid.
- **README per skill**: optional, when context beyond frontmatter is needed (tutorials, examples, caveats).
- **Line endings**: `.gitattribute` → `text=auto` for Git auto-normalization.
- **Empty SKILL.md files** = bugs (stubs). Note in README instead.

## Inventory

### `catalog.json` — repo contents inventory (auto-generated)

```json
{
  "generated": "2026-05-25T...",
  "sources": [
    {
      "name": "cantrips",
      "url": "file:///mnt/f/workspace/cantrips",
      "type": "local",
      "version": "0.0.0"
    },
    {
      "name": "agent-skills",
      "url": "https://github.com/vercel-labs/agent-skills",
      "type": "github",
      "version": "1.0.0"
    }
  ],
  "skills": [
    {
      "name": "skill-tree",
      "path": "skills/skill-tree/SKILL.md",
      "source": "cantrips",
      "version": null,
      "complexity": "playbook",
      "has_scripts": false,
      "has_references": false
    }
  ],
  "agents": [
    { "name": "rubber-duck", "path": "agents/rubber-duck.agent.md", "source": "cantrips", "git_sha": "abc1234" }
  ]
}
```

Rebuilt by `catalog.sh`. Single source of truth = repo on disk.

### `.env` / Config

#### `scripts/.env` — per-repo defaults

All in one shell file (no secrets). Flat key-value, no nested config. Comma-separated arrays use `,`.

```bash
SKILLS_PKG="skills@1.5.7"
INSTALL_TARGET=-g
INSTALL_AGENTS=
INSTALL_FLAT=
NPX_ARGS=
```

Overridable at runtime:

```bash
NPX_ARGS="-g -a opencode -a claude-code -y" ./scripts/skills.sh add vercel-labs/agent-skills my-skill
```

#### `~/.config/cantrips/registry.json` — per-machine state, _untracked_

Created by `init.sh` if it doesn't already exist.

```json
{
  "install_target": "-g",
  "npx_args": [],
  "sources": {},
  "installed_skills": {}
}
```

## Tooling

### `skills.sh` — primary command wrapper

Wraps `npx skills` + manages local cantrips skills via registry.

| Command | Usage | Behavior |
|---|---|---|
| `init` | `./skills.sh init` | Create registry, add cantrips as local source |
| `add` | `./skills.sh add <source> <skill>` | Add skill to registry, run `npx "$SKILLS_PKG" add --skill <name>` |
| `update` | `./skills.sh update [skill]` | Update specific or `--all` for every skill in registry |
| `remove` | `./skills.sh remove <skill>` | Remove skill from `~/.agents/skills/` + `skills-registry.json` |
| `sync` | `./skills.sh sync` | Walk `installed_skills`, run add for each |
| `ls` | `./skills.sh ls [flags]` | Pretty-print registry state |
| `find` | `./skills.sh find <query>` | Proxy to `npx skills find` |

Default install args: `"-g", "-a", "opencode", "-y"`.

### Flow

```
npx-installed:
  skills-registry.json → skills.sh → npx skills add/update/remove → ~/.agents/skills/

local-cantrips:
  skills-registry.json (local source entry) → skills.sh → npx skills add --skill <s> from /path/to/cantrips
```

Local skills are added to `skills-registry.json` like any other source — by directory path. `skills.sh` detects `type: "local"` and passes the directory to `npx skills add` instead of a GitHub URL.

### `catalog.sh` — rebuild catalog

Walks `skills/`, `agents/`, `archive/`. Never hand-edited.

### `init.sh` — one-shot setup

Clones/fetches cantrips repo → rebuilds catalog → syncs all skills in registry to `~/.agents/skills/`.

## Workflow

### Sync directions

```
cantrips/skills/    ← [npx add/update]── upstream repos (via registry)
cantrips/agents/    ← [local only]── your creations (git-tracked)
cantrips/archive/   ← [npx list]── new upstream, unreviewed → rename to skills/ after review
```

Pull only. Never auto-push. Local mods are git-tracked in cantrips.

### Add new skill (npx)

```bash
./scripts/skills.sh ls              # see what's installed
./scripts/skills.sh find typescript # discover new skills
./scripts/skills.sh add <source> <skill>  # adds to registry + installs
```

### Add new skill (local)

1. Create `skills/<name>/SKILL.md` (agentskills.io format)
2. `./scripts/skills.sh add /path/to/cantrips <skill-name>`
3. Commit as usual.

## Versioning

### Repo

No version number. Working collection, not a product.

### `.env` SKILLS_PKG

Pinned to exact semver: `skills@1.5.7`. Update manually when ready.

### Optional skill version (frontmatter)

```yaml
---
name: skill-tree
description: ...
version: 1.2.0
---
```

Convention only, not enforced. Used by skills.sh for merge priority.

### Registry timestamps

`skills-registry.json` tracks per-skill:
- `installed_at` — date of installation
- `version` — current version (or `null` for local)

## Hooks / CI

Local hooks only (no external CI).

### Pre-commit hook (optional)

Skips commits with files missing frontmatter or empty `SKILL.md`.

### Post-checkout hook (optional)

Rebuilds catalog. Warns if registry is stale.

### Installation

```bash
cp scripts/hooks/pre-commit .git/hooks/
cp scripts/hooks/post-checkout .git/hooks/
chmod +x .git/hooks/pre-commit .git/hooks/post-checkout
```

## Decisions

| ID | Decision | Rationale |
|---|---|---|
| D1 | Remote: `https://github.com/sprngr/cantrips.git` (manual push only) | Push at your discretion |
| D2 | Apply target: `~/.agents/skills/` | Unified, no dual WSL/Windows paths |
| D3 | `skills.sh` wraps `npx skills` CLI + manages registry | Single interface, leverage upstream tooling |
| D4 | `.env` for configurable defaults | Simple key-value, no YAML/JSON parsing needed |
| D5 | `catalog.json` is source of truth. `~/.config/cantrips/registry.json` is untracked per-machine state (no registry) |
| D6 | Nested `skills/` tree, scripts traverse recursively | Organizational structure, `npx skills add` handles extraction |
| D7 | `SKILL.md` is hard requirement | agentskills.io spec compliance |
| D8 | Dedup: existing in target dir wins, notify user | Never overwrite user modifications |
| D9 | Pin `SKILLS_PKG = "skills@1.5.7"` | Avoid supply chain drift, reproducible installs |
| D10 | `npx-registry.json` → `skills-registry.json` | Package is named `skills`, not `npx skills` |
| D11 | `apply.sh` removed | `skills.sh` handles local skills via registry |
| D12 | Pull only, no auto-push | Avoid conflicts with upstream, no conflicts at all |

## Open Questions

| ID | Question | Status |
|---|---|---|
| Q1 | When to push to GitHub? | After everything's done. Manual. |
| Q2 | Should `skills.sh` also update opencode `config.json` skill paths? | No — `skilling.sh` is the single source of truth, `npx skills` handles agent dirs |
| Q3 | Should `skills.sh` support `--copy` (copy over symlink)? | Maybe. Add as flag later if needed. |
| Q4 | How to handle `npx skills remove` for local skills? | Local skills stay in cantrips repo; remove only unlinks from `~/.agents/skills/`. Delete manually from cantrips if truly removing. |

## Next Steps

1. [x] Write PLAN.md (this document)
2. [x] Initial commit with PLAN.md, LICENSE, README.md
3. [ ] Write inventory/README.md (how to maintain inventory)
4. [ ] Write inventory/catalog.json initial structure
5. [ ] Write scripts/.env (SKILLS_PKG, install defaults)
6. [ ] Write scripts/skills.sh (add/update/remove/sync/ls/find/init)
7. [ ] Write scripts/catalog.sh (rebuild catalog.json)
8. [ ] Write scripts/init.sh (one-shot setup)
9. [ ] Final commit of everything
10. [ ] Push to `https://github.com/sprngr/cantrips.git`
