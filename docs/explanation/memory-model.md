# Memory Model

## Long-Term Memory

Markdown vault Markdown is canonical. It is human-readable, manually editable, and useful without LocalWeave.

## Operational Memory

The local database/index is derived state. It may include note metadata, headings, links, timestamps, checksums, and full-text search.

It can be deleted and rebuilt.

## Short-Term Memory

Session context is temporary unless the user approves saving a summary, decision, or project update to Markdown vault.

## Write Rule

LocalWeave should propose structured updates first. Approved writes may update narrow sections such as:

- Current State.
- Decisions.
- Next Actions.
- Resume Here.

## Offline Knowledge Library

The offline knowledge library is separate from Markdown vault.

Markdown vault stores personal memory, decisions, project state, and reflections. The offline library stores reference material such as programming docs, books, Wikipedia-style datasets, and research resources that LocalWeave can retrieve when internet access is unavailable.

Rules:

- Do not copy large reference libraries into Markdown vault.
- Keep indexes local and rebuildable.
- Track source, license, and update date for reference material.
- Prefer summaries and decisions in Markdown vault, not raw dumps.

## Voice Notes

Voice notes should become structured capture, not automatic memory.

Pipeline:

```text
recording -> transcript -> classification -> extracted ideas/tasks/decisions -> review -> approved Markdown vault update
```

The user decides whether a voice note becomes a daily note, project update, decision, learning note, or discarded ephemeral capture.
