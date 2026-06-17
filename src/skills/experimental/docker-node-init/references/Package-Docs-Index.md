# Package Docs Index

Build `docs-map` from selected stack values.

## Docker and boilerplate references

- Dockerfile Best Practices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- Docker Compose File Reference: https://docs.docker.com/compose/compose-file/
- Node.js Docker Official Image Guide: https://github.com/nodejs/docker-node/blob/main/README.md
- Twelve-Factor Config: https://12factor.net/config
- package.json spec: https://docs.npmjs.com/files/package.json

## Backend runtime and frameworks

- Node.js API docs: https://nodejs.org/docs/latest/api/
- Express: https://expressjs.com/
- Fastify: https://fastify.dev/docs/latest/
- Koa: https://koajs.com/
- Hono: https://hono.dev/docs/

## Frontend frameworks and tooling

- Vite guide: https://vite.dev/guide/
- React docs: https://react.dev/
- Vue guide: https://vuejs.org/guide/introduction.html
- Next.js docs: https://nextjs.org/docs
- Svelte docs: https://svelte.dev/docs
- Vanilla JS Architecture Wiki: https://github.com/olavgg/vanillajs

## Package managers

- npm CLI: https://docs.npmjs.com/cli/v10
- pnpm: https://pnpm.io/motivation
- Yarn: https://yarnpkg.com/getting-started

## Optional UI and architecture references

- Mantine: https://mantine.dev/
- Tailwind CSS: https://tailwindcss.com/docs
- Web Awesome: https://webawesome.com/docs

## Output rules

- Emit only links relevant to selected backend/frontend/package-manager stack.
- Keep URLs canonical and official where available.
- Inject selected links into `README.md` section `## Documentation links`.

## Asset routing notes

- Use `assets/package.json.tmpl` for baseline Node package manifest.
- Use `assets/Dockerfile.tmpl` for baseline API container build.
- Use `assets/docker-compose.yml.tmpl` for baseline service orchestration.
- Use `assets/.dockerignore.tmpl` and `assets/.gitignore.tmpl` for baseline ignore policy.
- Use `assets/.env.example.tmpl` for baseline environment variables.
- Use `assets/README.md.tmpl` for baseline project quickstart and docs-links section.
- Use backend starter assets per selected framework:
  - `assets/backend-express.tmpl`
  - `assets/backend-fastify.tmpl`
  - `assets/backend-koa.tmpl`
  - `assets/backend-hono.tmpl`
- Use frontend starter assets per selected framework:
  - `assets/frontend-react.tmpl`
  - `assets/frontend-vue.tmpl`
  - `assets/frontend-next.tmpl`
  - `assets/frontend-svelte.tmpl`
