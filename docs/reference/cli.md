# CLI Reference

## Setup And Health

`localweave init --vault PATH`

Creates or replaces the private local config with the Markdown vault path. The target must already be a directory.

`localweave doctor`

Checks private config, Markdown vault availability, runtime-directory access, `ffmpeg`, `whisper-cli`, and the configured speech model.

`localweave status`

Shows resolved repository, config, vault, data, state, cache, index, speech-engine, and write-policy status.

## Markdown Vault Retrieval

`localweave index`

Rebuilds the derived local SQLite/FTS5 index from Markdown notes. It does not write to the vault.

`localweave search QUERY [--limit N]`

Searches the current index. Default limit: `8`.

## Voice Queue

`localweave voice ingest PATH`

Copies a supported audio or transcript file into private LocalWeave storage. Text/Markdown inputs are marked transcribed immediately; audio is queued.

`localweave voice list`

Lists local voice items and states.

`localweave voice transcribe VOICE_ID`

Runs the configured local speech adapter. A missing engine leaves the item queued for retry.

`localweave voice propose VOICE_ID [--target RELATIVE_PATH]`

Creates a pending Markdown proposal. The default target is `Inbox.md` inside the configured vault.

## Proposals

`localweave proposal list`

Lists pending and applied proposals.

`localweave proposal show PROPOSAL_ID`

Shows proposal metadata, content, and the exact unified diff against the vault.

`localweave proposal apply PROPOSAL_ID --approve`

Applies one pending proposal. The target must remain inside the configured vault. Existing content is snapshotted first. Omitting `--approve` prints the diff and denies the write.

## Audit

`localweave audit [--limit N]`

Prints recent local audit events. Default limit: `20`.
