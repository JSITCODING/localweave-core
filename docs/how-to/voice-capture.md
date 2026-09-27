# Voice Capture

Voice capture is local and review-first. Recordings and transcripts remain in private application storage and never enter the repository.

## Install The Local Engine On macOS

```bash
brew install ffmpeg whisper-cpp
./scripts/install-whisper-model.sh
localweave doctor
```

The install script downloads the multilingual Whisper `base` model to LocalWeave private data and verifies its published SHA-1 checksum.

## Ingest A Recording

```bash
localweave voice ingest "/path/to/note.m4a"
```

Copy the printed `VOICE_ID`.

Supported audio: AAC, FLAC, M4A, MP3, OGG, WAV, and WebM. Existing `.txt` or `.md` transcripts can enter the same workflow.

## Transcribe Locally

```bash
localweave voice transcribe VOICE_ID
```

`whisper.cpp` receives normalized 16 kHz mono PCM and uses automatic language detection. If the engine is unavailable, the item remains queued instead of falling back to a cloud service.

## Create A Review Proposal

```bash
localweave voice propose VOICE_ID
```

The proposal contains a summary candidate, detected decisions/actions/ideas, and the transcript for review. Copy the printed `PROPOSAL_ID`.

## Review The Exact Change

```bash
localweave proposal show PROPOSAL_ID
```

Inspect the target, content, and unified diff. Do not apply a proposal with incorrect transcription or classification.

## Apply After Review

```bash
localweave proposal apply PROPOSAL_ID --approve
```

The target must resolve inside Markdown vault. If it already exists, LocalWeave creates a private snapshot before writing.

## Current Limitations

- Proposal editing and voice-item discard commands are not implemented yet.
- Heuristic extraction is not a semantic language model.
- Retention policy is not configurable yet.
- Accuracy has not yet been benchmarked on the user's real Portuguese/English recordings.

These limitations are Phase 1 work, not reasons to bypass review.
