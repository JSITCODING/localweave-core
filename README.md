# LocalWeave

LocalWeave is a local-first toolkit for private Markdown knowledge bases. Your vault remains the human-readable source of truth; LocalWeave adds retrieval, reviewed voice capture, permission checks, audit events, and recoverable proposed writes.

The repository is designed to be safe to share by default. Personal configuration, Markdown vault content, recordings, transcripts, proposals, snapshots, models, indexes, and audit history live outside the repository.

## Start Here

macOS development setup:

```bash
./scripts/bootstrap.sh
source .venv/bin/activate
localweave init --vault "/absolute/path/to/markdown-vault"
localweave doctor
localweave index
localweave search "current priorities"
```

For the complete first-run walkthrough, read [First Run](docs/tutorials/first-run.md). For every command, read the [CLI Reference](docs/reference/cli.md).

## Everyday Voice Workflow

```bash
localweave voice ingest "/path/to/note.m4a"
localweave voice transcribe VOICE_ID
localweave voice propose VOICE_ID
localweave proposal show PROPOSAL_ID
localweave proposal apply PROPOSAL_ID --approve
```

The final command is deliberately separate. No transcript becomes durable vault content until its proposal is reviewed and explicitly approved.

## Repository Shape

```text
src/localweave/
  app.py              composition root
  cli/                commands and user-facing output
  core/               stable permission and audit rules
  vault/              Markdown indexing and retrieval
  proposals/          review, diff, approval, and rollback
  runtime/            private config and runtime locations
  voice/              capture, queue, and transcription adapters
tests/
  unit/               fast tests by capability
  integration/        cross-capability workflows
docs/
  tutorials/          learn by completing a workflow
  how-to/             accomplish a specific task
  reference/          exact commands, config, and layout
  explanation/        architecture, product thinking, and vision
  security/           privacy, permissions, and threat model
  decisions/          architecture decision records
  roadmap/            milestones and long-term sequencing
scripts/              repeatable setup and verification commands
```

This is a modular monolith: one installable application with explicit internal capability boundaries. It is simpler to operate than separate services while allowing future modules such as `agents`, `knowledge`, `skills`, and `tools` to be added without enlarging the CLI or shared core indiscriminately.

## Privacy Boundary

Tracked repository:

- Source code, tests, safe examples, public-safe documentation, and dependency metadata.

Private application storage:

- Vault path and future credentials.
- Voice recordings and transcripts.
- Proposed writes and rollback snapshots.
- Local models and offline knowledge indexes.
- Audit history and operational state.
- Derived SQLite indexes and caches.
- Downloaded research references that should not be redistributed.

Run `localweave status` to see the resolved local locations. Read [Repository And Privacy Boundary](docs/security/repository-boundary.md) before adding any integration.

## Development

```bash
./scripts/check.sh
```

The check script runs tests, linting, and static type checks from the project virtual environment. See [Development Guide](docs/how-to/development.md) before changing a module boundary.

## Documentation

The documentation home is [docs/index.md](docs/index.md). The concrete build sequence is [Implementation Roadmap](docs/roadmap/implementation-roadmap.md), and architectural choices are recorded under [docs/decisions](docs/decisions/).

## Current Boundary

In scope now: local Markdown indexing/search, voice-note capture, local transcription, reviewable proposals, explicit approval, audit events, and rollback snapshots.

Out of scope now: always-listening audio, autonomous skill installation, unrestricted shell access, email sending, financial actions, broad computer control, and silent vault rewriting.
