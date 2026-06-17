---
name: docker-node-init
description: Generates dockerized Node.js boilerplate through guided init inputs, resolves template assets for core boilerplate files, and attaches official documentation links for selected stack packages/tools. Use when user asks to initialize new Node.js service with Docker and optional frontend scaffold.
---

Generate project boilerplate from guided init flow. Keep output deterministic from collected spec.

## When to use

- Use when user requests new dockerized Node.js starter.
- Use when user wants optional frontend starter in same project.
- Skip when user requests migration of existing non-boilerplate codebase.

## Instructions/Workflows

1. Collect init inputs from user. Produce JSON `init-spec.json` with keys `project_name`, `node_version`, `package_manager`, `backend_framework`, `port`, `frontend_choice`.
2. Validate `init-spec.json` against required keys in `references/Input-Spec.md`. Produce one line `spec_valid: true|false`.
3. Resolve boilerplate asset templates from `references/Boilerplate-Asset-Templates.md`. Produce `template-map` mapped to `assets/*.tmpl` for baseline files and selected framework starters.
4. Resolve official documentation references from `references/Package-Docs-Index.md`. Produce `docs-map` with canonical URLs for selected stack.
5. Resolve frontend decision from `frontend_choice` using `references/Frontend-Starter-Options.md`. Produce one line `frontend_plan: none|react|vue|next|svelte`.
6. Generate backend scaffold from `references/Backend-Scaffold-Playbook.md` and `template-map`. Produce files `package.json`, `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `.gitignore`.
7. Generate frontend scaffold when `frontend_plan` is not `none` using `references/Frontend-Starter-Options.md`. Produce `frontend/` tree and frontend Docker config.
8. Generate environment and docs from `references/Output-Contract.md` and `docs-map`. Produce `.env.example` and `README.md` with quickstart commands and docs references section.
9. Report setup summary to user. Produce sections `Created files`, `Run commands`, `Next steps`, `Frontend mode`, `Documentation links`.

## References

- See [Input-Spec.md](references/Input-Spec.md)
- See [Boilerplate-Asset-Templates.md](references/Boilerplate-Asset-Templates.md)
- See [Backend-Scaffold-Playbook.md](references/Backend-Scaffold-Playbook.md)
- See [Frontend-Starter-Options.md](references/Frontend-Starter-Options.md)
- See [Package-Docs-Index.md](references/Package-Docs-Index.md)
- See [assets/](assets/) for template asset files used by `template-map`
- See [Output-Contract.md](references/Output-Contract.md)
- See [Example.md](references/Example.md)
