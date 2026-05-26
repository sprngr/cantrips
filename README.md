# 🔮 Cantrips

Because I'm still not convinced this isn't magic.

A personal repository of agents, skills, and skill playbooks — original creations and curated finds from the web — synced across machines via lightweight scripts wrapping the [`skills`](https://www.npmjs.com/package/skills) npm package.

MIT licensed. Work for yourself, share for others.

## Structure

```
cantrips/
├── agents/           Agent definitions (*.agent.md), flat
├── skills/           Skills (nested tree; scripts traverse recursively)
├── archive/          Unreviewed upstream copies → rename to skills/ after review
├── inventory/        Machine-readable catalog (auto-generated)
│   └── catalog.json
└── scripts/          Setup and management scripts
    ├── skills.sh     Primary CLI wrapper
    ├── catalog.sh    Rebuild inventory/catalog.json
    └── init.sh       One-shot machine setup
```

## Conventions

- **Skill naming**: kebab-case (`skill-tree`, `duck-review`)
- **Agent naming**: kebab-case + emoji (`rubber-duck`)
- **SKILL.md**: hard requirement (agentskills.io spec). Skills without it are invalid.

## Inventory

`inventory/catalog.json` — auto-generated repo catalog. Do not hand-edit.

```bash
./scripts/catalog.sh   # rebuild
```

## Quick Start

```bash
# One-shot setup
bash scripts/init.sh

# Manage skills
./scripts/skills.sh ls        # see installed skills
./scripts/skills.sh find ts   # discover new skills
./scripts/skills.sh add <src> <name>    # add skill
./scripts/skills.sh update [skill]      # update (omit for all)
./scripts/skills.sh remove <name>       # remove skill
./scripts/skills.sh sync                # sync all registered

# Rebuild catalog
./scripts/catalog.sh
```

## Scripts

| Script | Purpose |
|-------------|-----------|
| `init.sh` | Clone/fetch repo → rebuild catalog → sync skills |
| `skills.sh` | Wrap `npx skills` CLI + manage local registry |
| `catalog.sh` | Walk `skills/`, `agents/`, `archive/` → `catalog.json` |

## Registry

Per-machine state lives at `~/.config/cantrips/registry.json` (untracked). Configurable defaults in `scripts/.env`.

Override at runtime:

```bash
NPX_ARGS="-g -y" ./scripts/skills.sh add vercel-labs/agent-skills my-skill
```

## Sync

```
cantrips/skills/  ← [npx add/update]── upstream repos (via registry)
cantrips/agents/  ← [local only]── your creations (git-tracked)
cantrips/archive/ ← [npx list]── new upstream, unreviewed → rename to skills/ after review
```

Pull only. Never auto-push.

## Versioning

- **Repo**: No version number. Working collection, not a product.
- **SKILLS_PKG**: Pinned to exact semver in `scripts/.env`
- **Optional skill version**: Add `version` in SKILL.md frontmatter (convention only)

## Adding a Local Skill

1. Create `skills/<name>/SKILL.md` (agentskills.io format)
2. `./scripts/skills.sh add /path/to/cantrips <name>`
3. Commit as usual.

## Adding a Skill from Upstream

```bash
./scripts/skills.sh ls
./scripts/skills.sh find typescript   # discover
./scripts/skills.sh add <source> <skill>
```
