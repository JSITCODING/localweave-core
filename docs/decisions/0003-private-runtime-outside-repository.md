# ADR 0003: Private Runtime Outside Repository

Status: accepted on 2026-08-21.

## Context

The original scaffold stored ignored models, indexes, logs, proposals, and voice directories beneath the checkout. Git ignored them, but repository copies, backup tools, support bundles, packaging mistakes, or a future remote workflow could still expose them. Tracked files also contained a real user path.

## Decision

Store only code, tests, safe examples, and public-safe documentation in the repository.

Use platform application locations for:

- Config: private configuration.
- Data: models, recordings, transcripts, proposals, snapshots, and future offline knowledge.
- State: audit and operational history.
- Cache: rebuildable indexes and derived artifacts.

Environment variables may override locations for testing and advanced operation. `localweave init` writes the normal private config with restrictive permissions.

## Consequences

- The working repository is safer to inspect, archive, or eventually share.
- Uninstalling source does not automatically delete personal data.
- Backup and retention policies can differ by data class.
- Tests must use temporary runtime roots.
- A migration is required whenever runtime path semantics change.
