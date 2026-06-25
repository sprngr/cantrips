# Input Spec

Collect inputs into `init-spec.json`.

## Required keys

- `project_name`: kebab-case service name.
- `node_version`: Node major version string (`18`, `20`, `22`).
- `package_manager`: one of `npm`, `pnpm`, `yarn`.
- `backend_framework`: one of `express`, `fastify`, `koa`, `hono`.
- `port`: integer service port.
- `frontend_choice`: one of `none`, `react`, `vue`, `next`, `svelte`.

## Validation rules

- Reject missing required keys.
- Reject unknown enum values.
- Reject non-integer `port`.
- Reject project names with spaces.

## Output contract

- Emit one line `spec_valid: true` when valid.
- Emit one line `spec_valid: false` plus list of missing/invalid keys when invalid.
