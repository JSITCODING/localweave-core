# Threat Model

Initial risks:

- Prompt injection from notes, email, web pages, or external data.
- Excessive context sent to cloud models.
- Silent or incorrect vault writes.
- Tool calls with too much permission.
- Secrets committed to git or exposed to models.
- Operational indexes becoming hidden memory.
- Accidental private-data exposure through a public repository or package build.

Initial controls:

- Public-safe generic core with private configuration, vault content, and runtime state stored outside the checkout.
- No secrets in git.
- No vault exports in git.
- Tool allowlists.
- Structured proposed operations.
- Human approval for writes and sensitive actions.
- Audit logs.
- Local-first routing where practical.
- Minimal cloud context.
