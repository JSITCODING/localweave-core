from __future__ import annotations

import difflib
import json
import shutil
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from localweave.core.audit import AuditLog
from localweave.core.permissions import Action, PermissionEngine

from .models import Proposal


class ProposalStore:
    def __init__(
        self,
        data_dir: Path,
        vault_path: Path,
        audit: AuditLog,
        permissions: PermissionEngine,
    ) -> None:
        self.directory = data_dir / "proposals"
        self.snapshots = data_dir / "snapshots"
        self.vault_path = vault_path.resolve()
        self.audit = audit
        self.permissions = permissions
        self.directory.mkdir(parents=True, exist_ok=True)
        self.snapshots.mkdir(parents=True, exist_ok=True)
        self.directory.chmod(0o700)
        self.snapshots.chmod(0o700)

    def create(
        self,
        *,
        kind: str,
        target: str,
        content: str,
        source: str,
        metadata: dict[str, Any] | None = None,
    ) -> Proposal:
        proposal = Proposal(
            id=uuid4().hex[:12],
            created_at=datetime.now(UTC).isoformat(),
            kind=kind,
            target=target,
            content=content,
            source=source,
            status="pending",
            metadata=metadata or {},
        )
        self._save(proposal)
        self.audit.record(
            "proposal.create",
            "success",
            {"proposal_id": proposal.id, "kind": kind, "target": target},
        )
        return proposal

    def list(self) -> list[Proposal]:
        return [self._load_path(path) for path in sorted(self.directory.glob("*.json"))]

    def load(self, proposal_id: str) -> Proposal:
        path = self.directory / f"{proposal_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Proposal not found: {proposal_id}")
        return self._load_path(path)

    def preview(self, proposal: Proposal) -> str:
        target = self._safe_target(proposal.target)
        old = target.read_text(encoding="utf-8") if target.exists() else ""
        new = self._merged_content(old, proposal.content)
        return "".join(
            difflib.unified_diff(
                old.splitlines(keepends=True),
                new.splitlines(keepends=True),
                fromfile=f"a/{proposal.target}",
                tofile=f"b/{proposal.target}",
            )
        )

    def apply(self, proposal_id: str, *, approved: bool) -> Path:
        proposal = self.load(proposal_id)
        if proposal.status != "pending":
            raise ValueError(f"Proposal is already {proposal.status}.")
        decision = self.permissions.evaluate(Action.WRITE_VAULT, approved=approved)
        if not decision.allowed:
            self.audit.record(
                "proposal.apply",
                "denied",
                {"proposal_id": proposal_id, "reason": decision.reason},
            )
            raise PermissionError(decision.reason)
        if proposal.kind != "append_markdown":
            raise ValueError(f"Unsupported proposal kind: {proposal.kind}")

        target = self._safe_target(proposal.target)
        target.parent.mkdir(parents=True, exist_ok=True)
        old = target.read_text(encoding="utf-8") if target.exists() else ""
        if target.exists():
            snapshot = self.snapshots / f"{proposal.id}.md"
            shutil.copy2(target, snapshot)
            snapshot.chmod(0o600)
        target.write_text(self._merged_content(old, proposal.content), encoding="utf-8")
        proposal.status = "applied"
        self._save(proposal)
        self.audit.record(
            "proposal.apply",
            "success",
            {"proposal_id": proposal.id, "target": proposal.target},
        )
        return target

    def _safe_target(self, relative: str) -> Path:
        candidate = (self.vault_path / relative).resolve()
        if not candidate.is_relative_to(self.vault_path):
            raise ValueError("Proposal target escapes the configured vault.")
        return candidate

    @staticmethod
    def _merged_content(old: str, addition: str) -> str:
        prefix = old.rstrip()
        if prefix:
            prefix += "\n\n"
        return prefix + addition.strip() + "\n"

    def _save(self, proposal: Proposal) -> None:
        path = self.directory / f"{proposal.id}.json"
        path.write_text(
            json.dumps(asdict(proposal), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        path.chmod(0o600)

    @staticmethod
    def _load_path(path: Path) -> Proposal:
        return Proposal(**json.loads(path.read_text(encoding="utf-8")))
