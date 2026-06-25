# Boilerplate Asset Templates

Map generated files to template assets.

## Required template-map keys

- `package.json`
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`
- `.gitignore`
- `.env.example`
- `README.md`

## Template-map format

Emit object with file key and template reference path.

```yaml
template_map:
  package.json: assets/package.json.tmpl
  Dockerfile: assets/Dockerfile.tmpl
  docker-compose.yml: assets/docker-compose.yml.tmpl
  .dockerignore: assets/.dockerignore.tmpl
  .gitignore: assets/.gitignore.tmpl
  .env.example: assets/.env.example.tmpl
  README.md: assets/README.md.tmpl
  backend.entry: assets/backend-<framework>.tmpl
  frontend.entry: assets/frontend-<framework>.tmpl
```

## Template requirements

- Parameterize project name, Node version, package manager, framework, and ports.
- Keep Docker base image aligned to selected Node major version.
- Keep compose service names stable: `api`, optional `frontend`.
- Keep README quickstart commands runnable without edits.
- Route backend starter selection to one of `assets/backend-express.tmpl`, `assets/backend-fastify.tmpl`, `assets/backend-koa.tmpl`, `assets/backend-hono.tmpl`.
- Route frontend starter selection to one of `assets/frontend-react.tmpl`, `assets/frontend-vue.tmpl`, `assets/frontend-next.tmpl`, `assets/frontend-svelte.tmpl`.
