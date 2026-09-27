from __future__ import annotations

import importlib.util
import shutil
import subprocess
import tempfile
from pathlib import Path

from .models import TEXT_EXTENSIONS


class TranscriberUnavailable(RuntimeError):
    pass


class LocalTranscriber:
    def __init__(self, model_name: str, model_path: Path | None = None) -> None:
        self.model_name = model_name
        self.model_path = model_path

    def engine(self) -> str | None:
        if (
            shutil.which("whisper-cli")
            and self.model_path is not None
            and self.model_path.is_file()
        ):
            return "whisper.cpp"
        if importlib.util.find_spec("faster_whisper") is not None:
            return "faster-whisper"
        return None

    def available(self) -> bool:
        return self.engine() is not None

    def transcribe(self, path: Path) -> str:
        if path.suffix.lower() in TEXT_EXTENSIONS:
            return path.read_text(encoding="utf-8").strip()
        engine = self.engine()
        if engine == "whisper.cpp":
            return self._transcribe_whisper_cpp(path)
        if engine != "faster-whisper":
            raise TranscriberUnavailable(
                "Local speech transcription is not ready. "
                "Run 'localweave doctor' for setup details."
            )
        from faster_whisper import WhisperModel  # type: ignore[import-not-found]

        model = WhisperModel(self.model_name, device="auto", compute_type="int8")
        segments, _ = model.transcribe(str(path), vad_filter=True)
        return " ".join(segment.text.strip() for segment in segments).strip()

    def _transcribe_whisper_cpp(self, path: Path) -> str:
        if self.model_path is None:
            raise TranscriberUnavailable("No whisper.cpp model path is configured.")
        whisper_cli = shutil.which("whisper-cli")
        ffmpeg = shutil.which("ffmpeg")
        if not whisper_cli or not ffmpeg:
            raise TranscriberUnavailable("whisper-cli and ffmpeg are required.")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temporary:
            wav_path = Path(temporary.name)
        try:
            conversion = subprocess.run(
                [
                    ffmpeg,
                    "-y",
                    "-i",
                    str(path),
                    "-ar",
                    "16000",
                    "-ac",
                    "1",
                    "-c:a",
                    "pcm_s16le",
                    str(wav_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if conversion.returncode != 0:
                raise ValueError("Audio conversion failed before transcription.")
            result = subprocess.run(
                [
                    whisper_cli,
                    "-m",
                    str(self.model_path),
                    "-f",
                    str(wav_path),
                    "-l",
                    "auto",
                    "-nt",
                    "-np",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                raise ValueError("Local Whisper transcription failed.")
            return result.stdout.strip()
        finally:
            wav_path.unlink(missing_ok=True)
