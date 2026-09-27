from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


class AuditLog:
    def __init__(self, path: Path) -> None:
        self.path = path

    def record(
        self,
        event: str,
        outcome: str,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.path.parent.chmod(0o700)
        entry = {
            "id": uuid4().hex,
            "timestamp": datetime.now(UTC).isoformat(),
            "event": event,
            "outcome": outcome,
            "details": details or {},
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=True) + "\n")
        self.path.chmod(0o600)
        return entry

    def tail(self, limit: int = 20) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8").splitlines()
        return [json.loads(line) for line in lines[-limit:]]
