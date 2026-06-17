# Backend Scaffold Playbook

Generate backend root files from `init-spec.json`.

## Files to produce

- `package.json`
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`
- `.gitignore`

## `package.json` requirements

- Set `name` from `project_name`.
- Set `engines.node` from `node_version`.
- Add scripts `dev`, `start`, `build`, `lint`, `test`.
- Add framework dependency from `backend_framework`.

## `Dockerfile` requirements

- Use `node:<node_version>-alpine` base.
- Set `WORKDIR /app`.
- Copy lockfile and install with selected `package_manager`.
- Copy source and expose `port`.
- Run service command from package manager scripts.

## `docker-compose.yml` requirements

- Define service `api`.
- Build from project root Dockerfile.
- Map host `port:port`.
- Load `.env` when present.
- Add volume mount for local development.

## Ignore files

- `.dockerignore`: `node_modules`, `.git`, `.env`, `coverage`, `dist`.
- `.gitignore`: `node_modules`, `.env`, `dist`, `coverage`, `.DS_Store`.
