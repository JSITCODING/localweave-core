from __future__ import annotations

import json
import re
import shutil
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from localweave.core.audit import AuditLog
from localweave.proposals import Proposal, ProposalStore

from .models import AUDIO_EXTENSIONS, TEXT_EXTENSIONS, VoiceItem
from .transcribers import LocalTranscriber, TranscriberUnavailable


class VoiceQueue:
    def __init__(
        self,
        data_dir: Path,
        audit: AuditLog,
        proposals: ProposalStore,
        model_name: str,
        model_path: Path | None = None,
    ) -> None:
        self.inbox = data_dir / "voice" / "inbox"
        self.queue = data_dir / "voice" / "queue"
        self.transcripts = data_dir / "voice" / "transcripts"
        self.audit = audit
        self.proposals = proposals
        self.transcriber = LocalTranscriber(model_name, model_path)
        for directory in (self.inbox, self.queue, self.transcripts):
            directory.mkdir(parents=True, exist_ok=True)
            directory.chmod(0o700)

    def ingest(self, source: Path) -> VoiceItem:
        source = source.expanduser().resolve()
        if not source.is_file():
            raise FileNotFoundError(f"Voice note not found: {source}")
        suffix = source.suffix.lower()
        if suffix not in AUDIO_EXTENSIONS | TEXT_EXTENSIONS:
            raise ValueError(f"Unsupported voice-note format: {suffix or 'no extension'}")

        item_id = uuid4().hex[:12]
        destination = self.inbox / f"{item_id}-{source.name}"
        shutil.copy2(source, destination)
        destination.chmod(0o600)
        item = VoiceItem(
            id=item_id,
            created_at=datetime.now(UTC).isoformat(),
            original_name=source.name,
            stored_path=str(destination),
            status="queued",
        )
        self._save(item)
        self.audit.record(
            "voice.ingest",
            "success",
            {"voice_id": item.id, "extension": suffix},
        )
        if suffix in TEXT_EXTENSIONS:
            return self.transcribe(item.id)
        return item

    def transcribe(self, item_id: str) -> VoiceItem:
        item = self.load(item_id)
        try:
            transcript = self.transcriber.transcribe(Path(item.stored_path))
            if not transcript:
                raise ValueError("The transcription was empty.")
            transcript_path = self.transcripts / f"{item.id}.txt"
            transcript_path.write_text(transcript + "\n", encoding="utf-8")
            transcript_path.chmod(0o600)
            item.transcript_path = str(transcript_path)
            item.status = "transcribed"
            item.error = None
            outcome = "success"
        except (TranscriberUnavailable, ValueError) as exc:
            item.status = "awaiting_transcriber"
            item.error = str(exc)
            outcome = "deferred"
        self._save(item)
        self.audit.record(
            "voice.transcribe",
            outcome,
            {"voice_id": item.id, "status": item.status},
        )
        return item

    def propose(
        self,
        item_id: str,
        target: str = "Inbox.md",
    ) -> Proposal:
        item = self.load(item_id)
        if item.status != "transcribed" or not item.transcript_path:
            raise ValueError("The voice note must be transcribed before review.")
        transcript = Path(item.transcript_path).read_text(encoding="utf-8").strip()
        proposal = self.proposals.create(
            kind="append_markdown",
            target=target,
            content=_capture_markdown(item, transcript),
            source=f"voice:{item.id}",
            metadata={"voice_id": item.id, "original_name": item.original_name},
        )
        item.proposal_id = proposal.id
        item.status = "proposed"
        self._save(item)
        self.audit.record(
            "voice.propose",
            "success",
            {"voice_id": item.id, "proposal_id": proposal.id},
        )
        return proposal

    def list(self) -> list[VoiceItem]:
        return [self._load_path(path) for path in sorted(self.queue.glob("*.json"))]

    def load(self, item_id: str) -> VoiceItem:
        path = self.queue / f"{item_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Voice item not found: {item_id}")
        return self._load_path(path)

    def _save(self, item: VoiceItem) -> None:
        path = self.queue / f"{item.id}.json"
        path.write_text(
            json.dumps(asdict(item), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        path.chmod(0o600)

    @staticmethod
    def _load_path(path: Path) -> VoiceItem:
        return VoiceItem(**json.loads(path.read_text(encoding="utf-8")))


def _capture_markdown(item: VoiceItem, transcript: str) -> str:
    sentences = [
        part.strip()
        for part in re.split(r"(?<=[.!?])\s+|\n+", transcript)
        if part.strip()
    ]
    summary = sentences[0] if sentences else transcript[:240]
    decisions = [
        line
        for line in sentences
        if re.search(r"\b(i|we) decided\b|^decision:", line, re.I)
    ]
    actions = [
        line
        for line in sentences
        if re.search(r"\b(i|we) need to\b|^todo:|^action:", line, re.I)
    ]
    ideas = [line for line in sentences if re.search(r"^idea:|\b(i|we) could\b", line, re.I)]

    def section(title: str, values: list[str]) -> list[str]:
        if not values:
            return []
        return [f"### {title}", *(f"- {value}" for value in values), ""]

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"## Voice capture - {timestamp}",
        "",
        f"Source: `{item.original_name}` (`{item.id}`)",
        "",
        "### Summary candidate",
        summary,
        "",
        *section("Potential decisions", decisions),
        *section("Potential actions", actions),
        *section("Potential ideas", ideas),
        "### Transcript for review",
        transcript,
    ]
    return "\n".join(lines)
