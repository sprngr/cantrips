# Output Contract

Return deterministic artifact summary after generation.

## Required summary sections

- `Created files`: grouped by backend and frontend.
- `Run commands`: exact shell commands to bootstrap and run.
- `Next steps`: short actionable checklist.
- `Frontend mode`: selected value and rationale.
- `Documentation links`: canonical references for selected tools/frameworks.

## Required generated files

- `.env.example`
- `README.md`

## `.env.example` requirements

- Include `NODE_ENV=development`.
- Include `PORT=<port from spec>`.
- Include placeholder DB/API keys only when used by chosen stack.

## `README.md` requirements

- State prerequisites (`docker`, `docker compose`).
- Provide startup commands.
- Provide logs and stop commands.
- Provide frontend URL when frontend enabled.
- Add section `## Documentation links` using selected entries from `docs-map`.

## Quickstart command template

```bash
docker compose build
docker compose up -d
docker compose logs -f api
```
