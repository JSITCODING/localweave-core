# Permission Model

The Permission Engine evaluates external actions and vault writes before execution.

## Tiers

| Tier | Examples | Default |
|---|---|---|
| Read-only | Search Markdown vault, read selected notes, inspect local metadata | Allow when scoped and logged |
| Ask first | Update Markdown vault, open a file, create a draft, move a file | Require explicit approval |
| Restricted | Send email, delete files, access sensitive integrations | Strong approval and narrow scope |
| Prohibited by default | Banking transactions, password disclosure, unrestricted shell | Not available |

## Rules

- Separate read, draft, write, send, delete, and financial capabilities.
- Treat retrieved note content as untrusted input.
- Never expose secrets directly to the model.
- Log approved actions and failures.
- Use structured proposed operations before writes.
- Show diffs before durable Markdown vault changes.

## Sandbox and Rollback Requirements

Actions that modify files, install skills, call external services, or run tools should execute through narrow adapters with explicit schemas.

Required controls:

- Allowlist tools by name and scope.
- Validate all tool arguments.
- Run risky or newly acquired skills in a sandbox first.
- Require approval before activation.
- Record audit events for proposals, approvals, denials, execution, and failures.
- Support rollback for durable vault writes.
- Keep unrestricted shell access prohibited by default.

Autonomous skill acquisition is a future capability, not an MVP shortcut.
