from __future__ import annotations

import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from localweave.cli.main import main


class CliSetupTests(unittest.TestCase):
    def test_init_then_status_uses_private_runtime_home(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            vault = root / "vault"
            vault.mkdir()
            runtime_home = root / "private-localweave"

            with (
                patch.dict("os.environ", {"LOCALWEAVE_HOME": str(runtime_home)}),
                redirect_stdout(StringIO()) as output,
            ):
                self.assertEqual(main(["init", "--vault", str(vault)]), 0)
                self.assertEqual(main(["status"]), 0)

            self.assertTrue((runtime_home / "config" / "config.toml").is_file())
            self.assertIn(str(runtime_home / "data"), output.getvalue())
            self.assertFalse(any(vault.rglob("*.md")))


if __name__ == "__main__":
    unittest.main()
