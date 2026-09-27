from __future__ import annotations

import stat
import tempfile
import unittest
from pathlib import Path

from localweave.core.audit import AuditLog
from localweave.vault import MarkdownVaultIndex


class MarkdownVaultIndexTests(unittest.TestCase):
    def test_rebuild_and_search(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            vault = root / "vault"
            vault.mkdir()
            (vault / "Project.md").write_text(
                "# LocalWeave Project\n\nVoice capture belongs in the first milestone.\n",
                encoding="utf-8",
            )
            audit_path = root / "data" / "audit.jsonl"
            index = MarkdownVaultIndex(
                vault,
                root / "data" / "vault.sqlite3",
                AuditLog(audit_path),
            )

            self.assertEqual(index.rebuild(), 1)
            results = index.search("voice milestone")

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].title, "LocalWeave Project")
            self.assertEqual(results[0].path, "Project.md")
            self.assertNotIn("voice milestone", audit_path.read_text(encoding="utf-8"))
            self.assertEqual(
                stat.S_IMODE(index.database_path.stat().st_mode), 0o600
            )
            self.assertEqual(stat.S_IMODE(audit_path.stat().st_mode), 0o600)
            self.assertEqual(
                stat.S_IMODE(index.database_path.parent.stat().st_mode), 0o700
            )
            self.assertEqual(stat.S_IMODE(audit_path.parent.stat().st_mode), 0o700)


if __name__ == "__main__":
    unittest.main()
