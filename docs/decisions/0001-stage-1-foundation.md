# Locked Decisions For Stage 1

Status: locked on 2026-08-20. These choices authorize the first local foundation; later milestones can revisit them through a documented decision.

## Architecture

- Runtime: Python 3.11-3.13, using the standard library wherever practical.
- First interface: CLI.
- Operational index: local SQLite with FTS5.
- Embeddings: excluded until measured retrieval gaps justify them.
- Markdown vault access: read-only by default; durable writes only through reviewed proposals.
- Model routing: local/retrieval-only in the first milestone. No cloud AI API is required.
- Voice: voice-note capture, transcription, and review are part of Stage 1. Always-listening and conversational voice are not.
- Transcription: a replaceable local adapter. The first engine is `whisper.cpp` with the multilingual `base` model; `faster-whisper` remains an optional alternative. Existing text transcripts work immediately, and audio remains queued when no engine is available.

## Permissions And Recovery

- Four tiers are confirmed: read-only, ask-first, restricted, and prohibited by default.
- Every vault write requires a structured proposal and explicit approval of that exact operation.
- Tool calls must be narrow, allowlisted, and argument-validated.
- Audit records cover reads, indexing, proposals, approvals, denials, writes, transcription, and failures without copying unnecessary sensitive content.
- Unrestricted shell, credential disclosure, banking actions, and destructive bulk actions remain prohibited by default.
- vault writes show a diff first and snapshot an existing target before mutation.
- All write targets must resolve inside the configured Markdown vault.

## Memory

- Markdown vault is canonical long-term memory.
- Operational indexes, queues, transcripts, proposals, audit records, and snapshots are local derived/runtime data and are excluded from Git.
- Raw external datasets do not enter Markdown vault.
- Voice notes enter a review queue and never become durable memory automatically.
- A voice proposal may be edited or discarded before approval; the transcript remains local runtime data.

## Repository

- Project location: a local checkout outside the Markdown vault.
- Repository mode: the generic core may be published, while all user data and runtime state remain local and untracked.
- Git remains useful for source history and rollback; repository publication never includes private runtime state.
- Secrets, `.env`, local indexes, audit logs, model caches, transcripts, proposals, snapshots, and copied Markdown vault content are excluded from commits.
- Committing remains a separate explicit action; implementation does not imply permission to commit.

## Infrastructure

- Current hardware is Node 0.
- No tower purchase is required for Stage 1.
- A future UPS is for graceful shutdown, data safety, and short outages.
- Building internet is not assumed to survive a power failure; cellular fallback and offline knowledge remain later infrastructure decisions.

## Product Boundary

- LocalWeave complements real life; it is not the user's primary life partner or purpose.
- Personality and companion behavior should increase agency and offline action, not dependency.
- Autonomous skill acquisition remains future-only and requires sandboxing, tests, approval, activation controls, and audit.
- Domain-specific tools should use reliable engines for state truth and the language layer for coaching.
