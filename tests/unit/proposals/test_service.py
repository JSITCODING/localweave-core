from __future__ import annotations

import stat
import tempfile
import unittest
from pathlib import Path

from localweave.core.audit import AuditLog
from localweave.core.permissions import PermissionEngine
from localweave.proposals import ProposalStore


class ProposalStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.vault = self.root / "vault"
        self.vault.mkdir()
        self.store = ProposalStore(
            self.root / "data",
            self.vault,
            AuditLog(self.root / "data" / "audit.jsonl"),
            PermissionEngine(),
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_apply_requires_approval_and_creates_snapshot(self) -> None:
        target = self.vault / "Inbox.md"
        target.write_text("# Inbox\n", encoding="utf-8")
        proposal = self.store.create(
            kind="append_markdown",
            target="Inbox.md",
            content="## Captured\nA reviewed note.",
            source="test",
        )

        with self.assertRaises(PermissionError):
            self.store.apply(proposal.id, approved=False)
        self.assertEqual(target.read_text(encoding="utf-8"), "# Inbox\n")

        self.store.apply(proposal.id, approved=True)
        self.assertIn("A reviewed note.", target.read_text(encoding="utf-8"))
        snapshot = self.root / "data" / "snapshots" / f"{proposal.id}.md"
        proposal_path = self.root / "data" / "proposals" / f"{proposal.id}.json"
        self.assertTrue(snapshot.exists())
        self.assertEqual(stat.S_IMODE(snapshot.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(proposal_path.stat().st_mode), 0o600)
        self.assertEqual(
            stat.S_IMODE((self.root / "data" / "proposals").stat().st_mode),
            0o700,
        )
        self.assertEqual(
            stat.S_IMODE((self.root / "data" / "snapshots").stat().st_mode),
            0o700,
        )

    def test_target_cannot_escape_vault(self) -> None:
        proposal = self.store.create(
            kind="append_markdown",
            target="../outside.md",
            content="no",
            source="test",
        )
        with self.assertRaises(ValueError):
            self.store.preview(proposal)


if __name__ == "__main__":
    unittest.main()
