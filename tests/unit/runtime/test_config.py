from __future__ import annotations

import stat
import tempfile
import unittest
from pathlib import Path

from localweave.runtime import Settings
from localweave.runtime.paths import RuntimePaths


class SettingsTests(unittest.TestCase):
    def test_private_config_and_runtime_data_stay_outside_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "repository"
            repository.mkdir()
            vault = root / "vault"
            vault.mkdir()
            paths = RuntimePaths(
                root / "private" / "config",
                root / "private" / "data",
                root / "private" / "state",
                root / "private" / "cache",
            )

            settings = Settings.load(repository, paths)
            config_path = settings.write_config(vault)
            settings.ensure_runtime_dirs()
            loaded = Settings.load(repository, paths)

            self.assertEqual(loaded.vault_path, vault.resolve())
            self.assertFalse(loaded.data_dir.is_relative_to(repository))
            self.assertEqual(stat.S_IMODE(config_path.stat().st_mode), 0o600)
            for directory in (
                settings.config_path.parent,
                settings.data_dir,
                settings.state_dir,
                settings.cache_dir,
            ):
                self.assertEqual(stat.S_IMODE(directory.stat().st_mode), 0o700)


if __name__ == "__main__":
    unittest.main()
