# Frontend Starter Options

Resolve frontend choice from `init-spec.json.frontend_choice`.

## Allowed choices

- `none`: skip frontend generation.
- `react`: create Vite React starter in `frontend/`.
- `vue`: create Vite Vue starter in `frontend/`.
- `next`: create Next.js starter in `frontend/`.
- `svelte`: create Vite Svelte starter in `frontend/`.

## Output rules

- Emit `frontend_plan: none|react|vue|next|svelte` before scaffold.
- Generate frontend only when value is not `none`.

## Files to produce when frontend enabled

- `frontend/package.json`
- `frontend/Dockerfile`
- `frontend/.dockerignore`
- framework starter files under `frontend/src/` or `frontend/app/`
- Compose service section for `frontend`

## Frontend Docker requirements

- Use Node image aligned to backend `node_version`.
- Expose frontend port (`5173` for Vite, `3001` for Next default in compose).
- Wire service dependency on `api` when backend URL needed.
