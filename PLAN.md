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
├── cantrips             ← thin CLI wrapper for cantrips.sh (symlinked to ~/.local/bin/)
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
│   ├── cantrips.sh      ← CLI router (routes → cantrips-skills.sh / cantrips-agents.sh / cantrips-catalog.sh)
│   ├── cantrips-skills.sh  ← npx skills CLI wrapper + local skill management
│   ├── cantrips-agents.sh ← agent file deployment per harness
│   ├── cantrips-catalog.sh ← rebuild inventory/catalog.json from repo state
│   ├── init.sh          ← one-shot machine setup
│   └── .env             ← configurable defaults (SKILLS_PKG, install_args, INSTALL_AGENTS)
└── archive/             ← unreviewed upstream copies to be moved to skills/ after review
```

### Directory semantics

| Directory | Purpose |
|---|-|
| `agents/` | Agent files. Flat. `name.agent.md`. |
| `skills/` | skills are nested. Scripts traverse recursively. |
| `archive/` | Skimmed upstream copies. Not vetted. | Same as `skills/` |
| `inventory/` | Machine-readable catalog (no registry) | `catalog.json` |
| `scripts/` | Bash scripts | `.sh`, POSIX-ish + GNU coreutils |

### Entry point: `cantrips`

Root `cantrips` file = thin POSIX wrapper. `cd` to script dir → exec `./scripts/cantrips.sh "$@"`.

`cantrips.sh` routes to `cantrips-skills.sh`, `cantrips-agents.sh`, or `cantrips-catalog.sh`. Only public executable the user needs.

Installation: `init.sh` symlinks `cantrips/` → `~/.local/bin/cantrips` (POSIX). On Windows/WSL: `New-Item` alias. `~/.local/bin` on PATH is standard on 99% of Linux distros.

## Conventions

- **Skill naming**: kebab-case (`skill-tree`, `duck-review`, `modify-memory`)
- **Agent naming**: kebab-case with emoji (`rubber-duck`, `code-architect`)
- **Frontmatter**: `SKILL.md` and `.agent.md` carry `---` frontmatter (`name`, `description`). Descriptions ≤ 1024 chars. Third person. Keyword triggers included.
- **`SKILL.md` hard requirement**: agentskills.io spec. Skills without it are invalid.
- **README per skill**: optional, when context beyond frontmatter is needed (tutorials, examples, caveats).
- **Line endings**: `.gitattribute` → `text=auto` for Git auto-normalization.
- **Empty SKILL.md files** = bugs (stubs). Note in README instead.

## Inventory

### `catalog.json` — 3rd-party curation manifest (auto-generated)

Lean install record. Re-add skills later. Not a registry.

```json
{
  "generated": "2026-05-25T...",
  "curations": [
    {
      "name": "agent-skills",
      "path": "skills/agent-skills/SKILL.md",
      "version": "1.0.0"
    }
  ]
}
```

Rebuilt by `cantrips catalog`.

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
NPX_ARGS="-g -a opencode -a claude-code -y" cantrips add vercel-labs/agent-skills my-skill
```

#### `~/.config/cantrips/` — clone directory for the repo

User installs cantrips repo here. `init.sh` creates this dir, clones repo, then places `skills-registry.json` inside it (untracked).

#### `~/.config/cantrips/skills-registry.json` — per-machine state, _untracked_

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

### `cantrips.sh` — CLI router

Routes subcommands to `cantrips-skills.sh`, `cantrips-agents.sh`, or `cantrips-catalog.sh`. Only public executable the user invokes.

| Subcommand | Usage | Routes to |
|---|---|---|
| `init` | `cantrips init` | `init.sh init` |
| `skills ls` | `cantrips skills ls` | `cantrips-skills.sh ls` |
| `skills add` | `cantrips skills add <source> <skill>` | `cantrips-skills.sh add` |
| `skills update` | `cantrips skills update [skill]` | `cantrips-skills.sh update` |
| `skills remove` | `cantrips skills remove <skill>` | `cantrips-skills.sh remove` |
| `skills sync` | `cantrips skills sync` | `cantrips-skills.sh sync` |
| `skills find` | `cantrips skills find <query>` | `cantrips-skills.sh find` |
| `catalog` | `cantrips catalog` | `cantrips-catalog.sh` |
| `agents sync` | `cantrips agents sync [harness]` | `cantrips-agents.sh sync` |
| `agents ls` | `cantrips agents ls` | `cantrips-agents.sh ls` |

### `cantrips-skills.sh` — npx skills CLI wrapper + registry management

Wraps npx skills + manages local cantrips skills via registry.

| Command | Usage | Behavior |
|---|---|---|
| `init` | `./cantrips-skills.sh init` | Create registry, add cantrips as local source |
| `add` | `./cantrips-skills.sh add <source> <skill>` | Add skill to registry, run `npx "$SKILLS_PKG" add --skill <name>` |
| `update` | `./cantrips-skills.sh update [skill]` | Update specific or `--all` for every skill in registry |
| `remove` | `./cantrips-skills.sh remove <skill>` | Remove skill from `~/.agents/skills/` + `skills-registry.json` |
| `sync` | `./cantrips-skills.sh sync` | Walk `installed_skills`, run add for each |
| `ls` | `./cantrips-skills.sh ls [flags]` | Pretty-print registry state |
| `find` | `./cantrips-skills.sh find <query>` | Proxy to `npx skills find` |

Fallback defaults if `.env` absent: `"-g", "-a", "opencode", "-y"`.

| `INSTALL_AGENTS` | Deploy agents? |
|---|-|
| `none` | Skip agent deployment |
| `auto` | Prompt user per harness at setup |
| `--all` | Deploy to all known harnesses |

### Flow

```
npx-installed:
  skills-registry.json → cantrips-skills.sh → npx skills add/update/remove → ~/.agents/skills/

local-cantrips:
  skills-registry.json (local source entry) → cantrips-skills.sh → npx skills add --skill <s> from /path/to/cantrips
```

Local skills are added to `skills-registry.json` like any other source — by directory path. `cantrips-skills.sh` detects `type: "local"` and passes the directory to `npx skills add` instead of a GitHub URL.

### `cantrips-agents.sh` — agent file deployment per harness

No universal harness agent directory exists. `cantrips-agents.sh` handles syncing `agents/*.agent.md` to harness-specific dirs. User picks known harness from a list at `--install` time. No auto-discovery — well-known list only.

| Command | Usage | Behavior |
|---|---|-|
| `sync` | `cantrips agents sync [harness]` | Symlink all agents to target dir; optional: `cantrips agents sync opencode claude` for select |
| `ls` | `cantrips agents ls` | List installed agents + their target dirs |
| `remove` | `cantrips agents remove <name>` | Unlink single agent from target |
| `remove-all` | `cantrips agents remove-all` | Unlink all agents |
| `list-harnesses` | `cantrips agents list-harnesses` | Show known harnesses + their agent directories |

Known harnesses (hardcoded list, extensible):

| Harness | Agent dir pattern | Config key |
|---|-|---|
| opencode | `~/.opencode/agents/` | `agentsDir` |
| claude-code | `~/.claude/agents/` | `agents` or `agentsDir` |
| copilot | `~/.copilot/agents/` | manual |
| codex | `~/.codex/agents/` | `agents-dir` |
| cursor | `~/.cursor/agents/` | `agentDirectory` |

Symlink default. Agent files stay in cantrips repo. `init.sh` runs `agents sync` if `INSTALL_AGENTS` is set.

| `.env` key | Values | Default |
|---|-|-|
| `INSTALL_AGENTS` | `auto` (prompt per harness), `none`, or `--all` | `none` |
| `AGENTS_EXCLUDE` | glob pattern, comma-separated | `*.template.md` |

### `cantrips-catalog.sh` — rebuild catalog

Walks `skills/`, `agents/`, `archive/`. Never hand-edited.

### `init.sh` — one-shot setup

Clones/fetches cantrips repo to `~/.config/cantrips/` → rebuilds catalog → creates `skills-registry.json` → symlinks `cantrips` to `~/.local/bin/cantrips` (or alias on Windows/WSL) → syncs all skills to `~/.agents/skills/` → if `INSTALL_AGENTS` is set, prompts user for targets then runs `cantrips-agents.sh sync` per selected harness.

## Workflow

### Sync directions

cantrips/
├── skills/        ← [npx add/update]── upstream repos (via registry)
├── agents/        ← [local only]── your creations (git-tracked)
└── archive/       ← [npx list]── new upstream, unreviewed → rename to skills/ after review

Pull only. Never auto-push. Local mods are git-tracked in cantrips.

### Add new skill (npx)

```bash
cantrips skills ls              # see what's installed
cantrips skills find typescript # discover new skills
cantrips skills add <source> <skill>  # adds to registry + installs
```

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
| D5 | `catalog.json` is source of truth. `~/.config/cantrips/skills-registry.json` is untracked per-machine state | clone dir houses both registry and repo |
| D6 | Nested `skills/` tree, scripts traverse recursively | Organizational structure, `npx skills add` handles extraction |
| D7 | `SKILL.md` is hard requirement | agentskills.io spec compliance |
| D8 | Dedup: existing in target dir wins, notify user | Never overwrite user modifications |
| D9 | Pin `SKILLS_PKG = "skills@1.5.7"` | Avoid supply chain drift, reproducible installs |
| D10 | `npx-registry.json` → `skills-registry.json` | Package is named `skills`, not `npx skills` |
| D11 | `apply.sh` removed | `cantrips-skills.sh` handles local skills via registry |
| D12 | Pull only, no auto-push | Avoid conflicts with upstream, no conflicts at all |
| D13 | `cantrips` CLI wrapper in repo root | Thin shim → `scripts/cantrips.sh`, symlinked to `~/.local/bin/` |
| D14 | `~/.config/cantrips/` is clone location | `init.sh` creates dir, clones repo, places registry inside |
| D15 | Wrapper + auto-symlink (not manual PATH) | `init.sh` handles it; `~/.local/bin` on PATH is standard |
| D16 | Windows/WSL symlink fallback | Uses `New-Item` alias on Windows, `ln -sf` on POSIX |
| D17 | `cantrips-agents.sh` separate from skills | Name parity, separate concern, no agent logic in `cantrips-skills.sh` |
| D18 | Sync agents = symlink default | Source of truth stays in repo; `—copy` available via flag |
| D19 | Agent deployment uses known harness list, not auto-discovery | User is primary user; known harnesses are stable, discovery is fragile |
| D20 | `INSTALL_AGENTS` in `.env` | `none`/`auto`/`--all`; prompts per harness if `auto` |

## Next Steps

1. [x] Write PLAN.md (this document)
2. [ ] Initial README.md
3. [ ] Write inventory/README.md (how to maintain inventory)
4. [ ] Write inventory/catalog.json initial structure
5. [ ] Write scripts/.env (SKILLS_PKG, install defaults)
6. [ ] Write scripts/cantrips-skills.sh (add/update/remove/sync/ls/find/init)
7. [ ] Write scripts/cantrips-catalog.sh (rebuild catalog.json)
6. [ ] Write scripts/cantrips-agents.sh
8. [ ] Write scripts/init.sh (one-shot setup)
9. [ ] Final README.md with workflow
