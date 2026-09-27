# ADR 0002: Modular Monolith

Status: accepted on 2026-08-21.

## Context

LocalWeave will eventually include retrieval, memory, voice, models, tools, skills, offline knowledge, interfaces, and background work. A flat package would make unrelated concerns depend on one another. Separate services would add deployment, networking, authentication, and operational complexity before those costs provide value.

## Decision

Build one installable Python application organized into capability packages with one composition root.

- Capability packages own their models, orchestration, and adapters.
- `app.py` constructs concrete services.
- The CLI dispatches to services but does not implement rules.
- Core rules remain small and dependency-light.
- Future capabilities become sibling packages only when their milestone starts.

## Consequences

- One command and one process remain easy to run locally.
- Capability boundaries can be tested independently.
- Adapters can change without rewriting user workflows.
- Some cross-capability imports remain; they must be explicit and reviewed.
- Splitting a module into a separate service is deferred until measured deployment or scaling needs justify it.
