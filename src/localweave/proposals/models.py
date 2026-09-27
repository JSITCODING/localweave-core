from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Proposal:
    id: str
    created_at: str
    kind: str
    target: str
    content: str
    source: str
    status: str
    metadata: dict[str, Any]
