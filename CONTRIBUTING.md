# Contributing

LocalWeave is an early-stage project. This guide defines the quality and privacy bar for proposed changes.

1. Read `docs/index.md`, the architecture, repository boundary, and current roadmap phase.
2. Keep each change inside one capability unless a documented interface must change.
3. Use synthetic data in tests and examples.
4. Add tests proportional to the permission, persistence, or integration risk.
5. Update task guides and CLI/config reference when behavior changes.
6. Record security-boundary or architecture changes in `docs/decisions/`.
7. Run `./scripts/check.sh` before considering the change complete.

Never commit private runtime data, even to a private remote.
