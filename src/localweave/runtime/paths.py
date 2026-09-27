from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuntimePaths:
    config_dir: Path
    data_dir: Path
    state_dir: Path
    cache_dir: Path

    @classmethod
    def for_current_user(cls) -> RuntimePaths:
        override = os.environ.get("LOCALWEAVE_HOME")
        if override:
            root = Path(override).expanduser().resolve()
            return cls(root / "config", root / "data", root / "state", root / "cache")

        home = Path.home()
        if sys.platform == "darwin":
            support = home / "Library" / "Application Support" / "LocalWeave"
            return cls(
                support / "config",
                support / "data",
                support / "state",
                home / "Library" / "Caches" / "LocalWeave",
            )

        config_home = Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
        data_home = Path(os.environ.get("XDG_DATA_HOME", home / ".local/share"))
        state_home = Path(os.environ.get("XDG_STATE_HOME", home / ".local/state"))
        cache_home = Path(os.environ.get("XDG_CACHE_HOME", home / ".cache"))
        return cls(
            config_home / "localweave",
            data_home / "localweave",
            state_home / "localweave",
            cache_home / "localweave",
        )
