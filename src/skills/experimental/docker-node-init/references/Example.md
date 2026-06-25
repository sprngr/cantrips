# Example: docker-node-init run with templates + docs map

## User request

"Create dockerized Node.js starter named `billing-api`, Node 20, npm, Express backend, port 3000, with React frontend. Include official docs links in README."

## Skill execution trace

1. Collected init inputs.
   Output (`init-spec.json`):
   ```json
   {
     "project_name": "billing-api",
     "node_version": "20",
     "package_manager": "npm",
     "backend_framework": "express",
     "port": 3000,
     "frontend_choice": "react"
   }
   ```

2. Validated required keys from `references/Input-Spec.md`.
   Output: `spec_valid: true`

3. Resolved boilerplate templates from `references/Boilerplate-Asset-Templates.md`.
   Output (`template-map`):
   - `package.json`: `assets/package.json.tmpl`
   - `Dockerfile`: `assets/Dockerfile.tmpl`
   - `docker-compose.yml`: `assets/docker-compose.yml.tmpl`
   - `.dockerignore`: `assets/.dockerignore.tmpl`
   - `.gitignore`: `assets/.gitignore.tmpl`
   - `.env.example`: `assets/.env.example.tmpl`
   - `README.md`: `assets/README.md.tmpl`
   - `backend.entry`: `assets/backend-express.tmpl`
   - `frontend.entry`: `assets/frontend-react.tmpl`

4. Resolved official docs from `references/Package-Docs-Index.md`.
   Output (`docs-map`):
   - Node.js: `https://nodejs.org/docs/latest/api/`
   - Dockerfile best practices: `https://docs.docker.com/develop/develop-images/dockerfile_best-practices/`
   - Docker Compose spec: `https://docs.docker.com/compose/compose-file/`
   - npm CLI: `https://docs.npmjs.com/cli/v10`
   - Express: `https://expressjs.com/`
   - React: `https://react.dev/`
   - Vite: `https://vite.dev/guide/`
   - Twelve-Factor config: `https://12factor.net/config`

5. Resolved frontend mode from `references/Frontend-Starter-Options.md`.
   Output: `frontend_plan: react`

6. Generated backend scaffold from playbook + templates.
   Output files:
   - `package.json`
   - `Dockerfile`
   - `docker-compose.yml`
   - `.dockerignore`
   - `.gitignore`

7. Generated frontend scaffold for React.
   Output files:
   - `frontend/package.json`
   - `frontend/src/main.jsx`
   - `frontend/Dockerfile`
   - `frontend/.dockerignore`

8. Generated docs/env with docs-map injection.
   Output files:
   - `.env.example`
   - `README.md` (includes `## Documentation links` section)

9. Reported setup summary.
   Output sections:
   - Created files
   - Run commands
   - Next steps
   - Frontend mode
   - Documentation links

## Edge case correction

Input failure:
```json
{
  "project_name": "billing api",
  "node_version": "20",
  "package_manager": "npm",
  "backend_framework": "express",
  "port": "3000",
  "frontend_choice": "react"
}
```

Validation result: `spec_valid: false`  
Invalid fields: `project_name` (contains space), `port` (not integer)  
Correction applied: normalized name to `billing-api`, cast port to integer `3000`, resumed generation.

## Concrete final output

Quickstart commands in `README.md`:

```bash
docker compose build
docker compose up -d
docker compose logs -f api
docker compose logs -f frontend
```

README docs section includes canonical URLs for chosen stack.

### Agent-calibration notes

- Tone: direct, terse, action-first.
- Pacing: ask for missing keys only; avoid re-asking complete fields.
- Output shape: emit `template-map` and `docs-map` before file generation.
