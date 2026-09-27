# First Run

This tutorial takes a new local checkout from zero to a searchable Markdown vault and a reviewable voice proposal. It does not write to Markdown vault.

## 1. Create The Development Environment

From the repository root:

```bash
./scripts/bootstrap.sh
source .venv/bin/activate
```

This creates an isolated Python environment, installs LocalWeave in editable mode, and installs development checks.

## 2. Configure The Vault Privately

```bash
localweave init --vault "/absolute/path/to/Markdown vault"
```

The command stores the vault path in an owner-readable config file outside the repository. Do not add the real path to `.env.example`, README files, tests, or source code.

## 3. Check The Machine

```bash
localweave doctor
```

Every line should say `OK`. If the speech engine or model is missing, follow the voice setup in [Voice Capture](../how-to/voice-capture.md).

## 4. Build The Local Search Index

```bash
localweave index
```

The SQLite index is rebuildable cache data. Markdown vault remains unchanged.

## 5. Search Markdown vault

```bash
localweave search "current priorities"
```

Results include the note title, relative source path, and an excerpt. Search text is fingerprinted rather than copied into the audit log.

## 6. Try The Review Queue Without Audio

```bash
localweave voice ingest examples/sample_voice_note.txt
localweave voice list
```

The command prints a `VOICE_ID`. Use it in the next command:

```bash
localweave voice propose VOICE_ID
```

The command prints a `PROPOSAL_ID`. Review it:

```bash
localweave proposal show PROPOSAL_ID
```

Stop here for the tutorial. No Markdown vault file has been changed. Applying requires a separate command with `--approve`.

## 7. Verify The Project

```bash
./scripts/check.sh
```

You now have a configured, searchable, locally tested LocalWeave installation with a functioning review boundary.
