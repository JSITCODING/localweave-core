from __future__ import annotations

import hashlib
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from localweave.core.audit import AuditLog


@dataclass(frozen=True)
class SearchResult:
    path: str
    title: str
    excerpt: str
    score: float


def _title_for(path: Path, content: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def _markdown_files(vault_path: Path) -> list[Path]:
    return sorted(
        path
        for path in vault_path.rglob("*.md")
        if not any(part.startswith(".") for part in path.relative_to(vault_path).parts)
    )


class MarkdownVaultIndex:
    def __init__(self, vault_path: Path, database_path: Path, audit: AuditLog) -> None:
        self.vault_path = vault_path.resolve()
        self.database_path = database_path
        self.audit = audit

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.database_path.parent.chmod(0o700)
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                path TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                modified_ns INTEGER NOT NULL,
                checksum TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts
            USING fts5(path UNINDEXED, title, body)
            """
        )
        self._secure_database_files()
        return connection

    def _secure_database_files(self) -> None:
        for path in (
            self.database_path,
            Path(f"{self.database_path}-wal"),
            Path(f"{self.database_path}-shm"),
        ):
            if path.exists():
                path.chmod(0o600)

    def rebuild(self) -> int:
        if not self.vault_path.is_dir():
            self.audit.record(
                "vault.index", "failed", {"reason": "vault_missing"}
            )
            raise FileNotFoundError(f"Markdown vault not found: {self.vault_path}")

        files = _markdown_files(self.vault_path)
        with self._connect() as connection:
            connection.execute("DELETE FROM notes")
            connection.execute("DELETE FROM notes_fts")
            for path in files:
                body = path.read_text(encoding="utf-8")
                relative = path.relative_to(self.vault_path).as_posix()
                title = _title_for(path, body)
                checksum = hashlib.sha256(body.encode("utf-8")).hexdigest()
                modified_ns = path.stat().st_mtime_ns
                connection.execute(
                    "INSERT INTO notes VALUES (?, ?, ?, ?, ?)",
                    (relative, title, body, modified_ns, checksum),
                )
                connection.execute(
                    "INSERT INTO notes_fts(path, title, body) VALUES (?, ?, ?)",
                    (relative, title, body),
                )
        self.audit.record("vault.index", "success", {"note_count": len(files)})
        self._secure_database_files()
        return len(files)

    def search(self, query: str, limit: int = 8) -> list[SearchResult]:
        tokens = re.findall(r"\w+", query, flags=re.UNICODE)
        if not tokens:
            return []
        fts_query = " AND ".join(f'"{token}"' for token in tokens)
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT path, title,
                       snippet(notes_fts, 2, '[', ']', '...', 20) AS excerpt,
                       bm25(notes_fts) AS score
                FROM notes_fts
                WHERE notes_fts MATCH ?
                ORDER BY score
                LIMIT ?
                """,
                (fts_query, limit),
            ).fetchall()
        self.audit.record(
            "vault.search",
            "success",
            {
                "query_fingerprint": hashlib.sha256(query.encode("utf-8")).hexdigest()[:12],
                "result_count": len(rows),
            },
        )
        self._secure_database_files()
        return [SearchResult(**dict(row)) for row in rows]
