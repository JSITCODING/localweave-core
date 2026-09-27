from dataclasses import dataclass

TEXT_EXTENSIONS = {".txt", ".md"}
AUDIO_EXTENSIONS = {".aac", ".flac", ".m4a", ".mp3", ".ogg", ".wav", ".webm"}


@dataclass
class VoiceItem:
    id: str
    created_at: str
    original_name: str
    stored_path: str
    status: str
    transcript_path: str | None = None
    proposal_id: str | None = None
    error: str | None = None
