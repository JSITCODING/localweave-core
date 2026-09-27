from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .paths import RuntimePaths


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _read_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _nested(config: dict[str, Any], section: str, key: str) -> str | None:
    value = config.get(section, {}).get(key)
    return str(value) if value is not None else None


def _default_vault_path() -> Path:
    home = Path.home()
    return home / "Documents" / "LocalWeaveVault"


def _resolve_path(raw: str | None, default: Path) -> Path:
    return Path(raw).expanduser().resolve() if raw else default.resolve()


@dataclass(frozen=True)
class Settings:
    repo_root: Path
    config_path: Path
    vault_path: Path
    data_dir: Path
    state_dir: Path
    cache_dir: Path
    whisper_model: str = "base"
    whisper_model_path: Path | None = None

    @classmethod
    def load(
        cls,
        repo_root: Path | None = None,
        runtime_paths: RuntimePaths | None = None,
    ) -> Settings:
        root = (repo_root or _repo_root()).resolve()
        paths = runtime_paths or RuntimePaths.for_current_user()
        config_path = _resolve_path(
            os.environ.get("LOCALWEAVE_CONFIG_PATH"), paths.config_dir / "config.toml"
        )
        config = _read_config(config_path)

        data_dir = _resolve_path(
            os.environ.get("LOCALWEAVE_DATA_DIR")
            or _nested(config, "runtime", "data_dir"),
            paths.data_dir,
        )
        state_dir = _resolve_path(
            os.environ.get("LOCALWEAVE_STATE_DIR")
            or _nested(config, "runtime", "state_dir"),
            paths.state_dir,
        )
        cache_dir = _resolve_path(
            os.environ.get("LOCALWEAVE_CACHE_DIR")
            or _nested(config, "runtime", "cache_dir"),
            paths.cache_dir,
        )
        model_path = _resolve_path(
            os.environ.get("LOCALWEAVE_WHISPER_MODEL_PATH")
            or _nested(config, "voice", "model_path"),
            data_dir / "models" / "ggml-base.bin",
        )

        return cls(
            repo_root=root,
            config_path=config_path,
            vault_path=_resolve_path(
                os.environ.get("LOCALWEAVE_VAULT_PATH")
                or _nested(config, "vault", "path"),
                _default_vault_path(),
            ),
            data_dir=data_dir,
            state_dir=state_dir,
            cache_dir=cache_dir,
            whisper_model=os.environ.get("LOCALWEAVE_WHISPER_MODEL")
            or _nested(config, "voice", "model")
            or "base",
            whisper_model_path=model_path,
        )

    @property
    def index_path(self) -> Path:
        return self.cache_dir / "indexes" / "vault.sqlite3"

    @property
    def audit_path(self) -> Path:
        return self.state_dir / "audit" / "events.jsonl"

    def ensure_runtime_dirs(self) -> None:
        for path in (
            self.config_path.parent,
            self.data_dir,
            self.state_dir,
            self.cache_dir,
            self.cache_dir / "indexes",
            self.state_dir / "audit",
            self.data_dir / "proposals",
            self.data_dir / "snapshots",
            self.data_dir / "models",
            self.data_dir / "voice" / "inbox",
            self.data_dir / "voice" / "queue",
            self.data_dir / "voice" / "transcripts",
        ):
            path.mkdir(parents=True, exist_ok=True, mode=0o700)
            path.chmod(0o700)

    def write_config(self, vault_path: Path) -> Path:
        vault = vault_path.expanduser().resolve()
        if not vault.is_dir():
            raise FileNotFoundError(f"Markdown vault not found: {vault}")
        self.config_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.config_path.parent.chmod(0o700)
        escaped = str(vault).replace("\\", "\\\\").replace('"', '\\"')
        content = (
            "# LocalWeave configuration. Keep this file outside source control.\n\n"
            "[vault]\n"
            f'path = "{escaped}"\n\n'
            "[voice]\n"
            'model = "base"\n'
        )
        self.config_path.write_text(content, encoding="utf-8")
        self.config_path.chmod(0o600)
        return self.config_path
