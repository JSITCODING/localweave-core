# Development Guide

## Set Up

```bash
./scripts/bootstrap.sh
source .venv/bin/activate
```

## Run All Checks

```bash
./scripts/check.sh
```

The script runs unit/integration tests, Ruff, and mypy. A change is not complete until these checks pass or a documented reason explains why a check cannot run.

## Choose The Correct Module

- CLI parsing or output: `src/localweave/cli/`.
- Shared stable rule: `src/localweave/core/`.
- Markdown vault indexing/retrieval: `src/localweave/vault/`.
- Proposal review/write/rollback: `src/localweave/proposals/`.
- Config or filesystem locations: `src/localweave/runtime/`.
- Voice capture/transcription: `src/localweave/voice/`.
- Wiring between capabilities: `src/localweave/app.py` only.

Do not put feature logic in the CLI or composition root. Do not put filesystem, SQLite, subprocess, or network operations into permission rules or data models.

## Add A Capability

1. Write the user outcome and risk boundary in the roadmap or a decision record.
2. Create a capability package only when the behavior is real; do not create empty future folders.
3. Put data models and pure rules in small modules.
4. Put operating-system or service-specific code behind a named adapter.
5. Wire the adapter in `app.py`.
6. Add unit tests for rules and integration tests for cross-capability behavior.
7. Update the CLI reference and one task-oriented guide.
8. Run `./scripts/check.sh`.

## Change A Security Boundary

Any change that adds a write, send, delete, credential, network, shell, background, or financial capability requires:

1. Threat-model update.
2. Permission tier.
3. Narrow argument schema.
4. Approval behavior.
5. Audit behavior.
6. Failure and rollback behavior.
7. Tests proving denial and containment.
8. A decision record before activation.
