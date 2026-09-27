# Repository Layout

## Top Level

| Path | Responsibility | May contain personal data? |
|---|---|---|
| `src/localweave/` | Installable application code | No |
| `tests/` | Synthetic test data and behavior checks | No |
| `docs/` | Public-safe project documentation | No |
| `examples/` | Small fictional/sanitized inputs | No |
| `scripts/` | Repeatable setup and verification | No |
| `pyproject.toml` | Package and tooling metadata | No |
| `.env.example` | Placeholder variable names | No real values |

## Application Package

| Path | Responsibility | Depends on |
|---|---|---|
| `app.py` | Composition root; constructs services | All concrete capabilities |
| `cli/` | Parse commands and render results | Composition root and public service APIs |
| `core/` | Stable permissions and audit contract | Python standard library only |
| `vault/` | Markdown discovery, SQLite indexing, retrieval | Core audit |
| `proposals/` | Proposal models, diffs, approval, writes, snapshots | Core permissions and audit |
| `runtime/` | Config loading, platform paths, private directories | Standard library only |
| `voice/` | Voice models, queue, capture formatting, speech adapters | Proposals and core audit |

## Dependency Rules

- `app.py` may know concrete implementations; feature modules must not import the CLI.
- CLI code contains presentation and dispatch, not business rules.
- Models must not perform filesystem, database, subprocess, or network operations.
- A platform adapter can be replaced without changing the calling workflow.
- Capability-to-capability dependencies must be explicit imports, not shared global state.
- New top-level capability packages require implemented behavior and tests, not speculative folders.

## Future Packages

Add only when their milestone begins:

- `agents/`: orchestration and model routing.
- `knowledge/`: offline reference ingestion and retrieval.
- `skills/`: skill manifests, sandboxing, activation, and lifecycle.
- `tools/`: narrow external action adapters.
- `interfaces/`: web, desktop, or mobile interfaces if CLI is no longer the only interface.
