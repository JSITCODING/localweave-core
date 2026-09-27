from __future__ import annotations

import stat
import tempfile
import unittest
from pathlib import Path

from localweave.core.audit import AuditLog
from localweave.core.permissions import PermissionEngine
from localweave.proposals import ProposalStore
from localweave.voice import VoiceQueue


class VoiceQueueTests(unittest.TestCase):
    def test_transcript_enters_review_queue_before_vault(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            vault = root / "vault"
            vault.mkdir()
            data = root / "data"
            audit = AuditLog(data / "audit.jsonl")
            proposals = ProposalStore(data, vault, audit, PermissionEngine())
            queue = VoiceQueue(data, audit, proposals, "small")
            source = root / "note.txt"
            source.write_text(
                "Idea: we could review the project backlog. "
                "I need to schedule the first review.",
                encoding="utf-8",
            )

            item = queue.ingest(source)
            self.assertEqual(item.status, "transcribed")
            self.assertFalse(any(vault.rglob("*.md")))

            proposal = queue.propose(item.id)
            self.assertEqual(proposal.status, "pending")
            self.assertIn("Potential ideas", proposal.content)
            self.assertIn("Potential actions", proposal.content)
            self.assertFalse(any(vault.rglob("*.md")))

            private_files = (
                Path(item.stored_path),
                Path(item.transcript_path or ""),
                queue.queue / f"{item.id}.json",
                proposals.directory / f"{proposal.id}.json",
                data / "audit.jsonl",
            )
            for path in private_files:
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            for directory in (queue.inbox, queue.queue, queue.transcripts):
                self.assertEqual(stat.S_IMODE(directory.stat().st_mode), 0o700)


if __name__ == "__main__":
    unittest.main()
