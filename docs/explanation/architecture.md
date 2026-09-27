# LocalWeave Architecture

LocalWeave is a modular local application around replaceable models and adapters. Markdown vault remains durable canonical memory.

```text
Markdown vault = human-readable source of truth
LocalWeave = optional retrieval, reasoning, interface, permission, and tool layer
```

## System Context

```mermaid
flowchart LR
    User["User"] --> CLI["LocalWeave CLI"]
    CLI --> App["Composition Root"]
    App --> Markdown vault["Markdown vault Capability"]
    App --> Voice["Voice Capability"]
    App --> Proposals["Proposal Capability"]
    App --> Core["Permissions and Audit"]
    Markdown vault --> Vault[("Markdown vault Markdown")]
    Markdown vault --> Cache[("Derived Search Cache")]
    Voice --> Speech["Local Speech Adapter"]
    Voice --> PrivateData[("Private Voice Data")]
    Voice --> Proposals
    Proposals --> Vault
    Proposals --> PrivateData
```

The language model is intentionally absent from the current runtime. When added, it will call application capabilities through narrow interfaces; it will not become the permission engine, filesystem, database, or source of truth.

## Modular Monolith

LocalWeave is one installable package and one local process. Internal packages are organized by capability:

- `cli`: commands and presentation.
- `core`: stable permission and audit rules.
- `vault`: Markdown indexing and retrieval.
- `proposals`: review, diff, approval, write containment, and snapshots.
- `runtime`: private config and platform data locations.
- `voice`: capture queue, transcript formatting, and local speech adapters.
- `app.py`: composition root that wires concrete services.

This keeps operation simple while preventing a single `localweave.py` or `services.py` from accumulating unrelated logic.

## Dependency Direction

```text
CLI -> composition root -> capability services
capability services -> core rules and named adapters
models -> standard library only
```

Rules:

- The CLI may not perform durable writes directly.
- The model layer may not decide authorization.
- Runtime configuration may not import feature behavior.
- Capabilities may collaborate through explicit service APIs.
- Platform-specific code remains replaceable and testable.
- No hidden singleton or mutable global owns user state.

## Data Classes

| Class | Location | Examples | Repository? |
|---|---|---|---|
| Canonical memory | Markdown vault | projects, decisions, areas | Separate vault |
| Durable private data | LocalWeave data home | recordings, transcripts, models, proposals, snapshots | Never |
| Operational state | LocalWeave state home | audit history, future job state | Never |
| Rebuildable cache | LocalWeave cache home | SQLite FTS index, future embeddings | Never |
| Source artifacts | repository | code, tests, safe docs/examples | Yes |

Private storage remains outside the checkout regardless of whether the generic core is published.

## Current Request Flow

Markdown vault search:

```text
command -> index service -> SQLite FTS -> source-linked result -> audit metadata
```

Voice capture:

```text
recording -> private queue -> local speech adapter -> private transcript
          -> structured proposal -> diff review -> explicit approval
          -> contained vault write + snapshot + audit event
```

## Future Expansion

Future sibling capabilities may include:

- `agents`: session orchestration and model routing.
- `knowledge`: licensed offline reference ingestion and retrieval.
- `skills`: manifests, sandbox tests, activation, and disable lifecycle.
- `tools`: narrow external adapters with typed side effects.
- `interfaces`: web, desktop, mobile, and conversational voice.

They should be added one milestone at a time. A separate process or service is justified only by measured isolation, deployment, reliability, or scaling requirements.

## Safety Architecture

- Retrieved content is untrusted input.
- Model output is untrusted input.
- Authorization is deterministic application code.
- Durable actions require typed proposals.
- High-impact actions require human approval.
- Paths and arguments are validated at adapter boundaries.
- Every durable action must define failure and recovery behavior.
- Operational indexes remain rebuildable.
