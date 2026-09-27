# Configuration Reference

## Normal Setup

Use:

```bash
localweave init --vault "/absolute/path/to/markdown-vault"
```

On macOS, LocalWeave stores its private configuration beneath `~/Library/Application Support/LocalWeave/config/`. The config file is created with owner-only read/write permissions.

## Runtime Separation

On macOS:

- Config: `~/Library/Application Support/LocalWeave/config/`
- Durable private data: `~/Library/Application Support/LocalWeave/data/`
- Audit and operational state: `~/Library/Application Support/LocalWeave/state/`
- Rebuildable index/cache: `~/Library/Caches/LocalWeave/`

On Linux, LocalWeave follows XDG config, data, state, and cache locations.

## Precedence

Highest to lowest:

1. Process environment variables.
2. Private `config.toml`.
3. Platform defaults. The default vault path is `~/Documents/LocalWeaveVault` until configured.

## Environment Overrides

- `LOCALWEAVE_CONFIG_PATH`
- `LOCALWEAVE_HOME`
- `LOCALWEAVE_DATA_DIR`
- `LOCALWEAVE_STATE_DIR`
- `LOCALWEAVE_CACHE_DIR`
- `LOCALWEAVE_VAULT_PATH`
- `LOCALWEAVE_WHISPER_MODEL`
- `LOCALWEAVE_WHISPER_MODEL_PATH`

`LOCALWEAVE_HOME` is useful for tests or a portable isolated installation. It creates `config`, `data`, `state`, and `cache` beneath one absolute path.

Do not place real values in tracked files. `.env.example` documents names only; it is not the normal storage mechanism.
