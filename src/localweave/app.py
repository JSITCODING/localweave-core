from __future__ import annotations

from dataclasses import dataclass

from .core.audit import AuditLog
from .core.permissions import PermissionEngine
from .proposals import ProposalStore
from .runtime import Settings
from .vault import MarkdownVaultIndex
from .voice import VoiceQueue


@dataclass(frozen=True)
class Services:
    settings: Settings
    audit: AuditLog
    permissions: PermissionEngine
    proposals: ProposalStore
    voice: VoiceQueue
    index: MarkdownVaultIndex

    @classmethod
    def build(cls, settings: Settings) -> Services:
        settings.ensure_runtime_dirs()
        audit = AuditLog(settings.audit_path)
        permissions = PermissionEngine()
        proposals = ProposalStore(
            settings.data_dir,
            settings.vault_path,
            audit,
            permissions,
        )
        voice = VoiceQueue(
            settings.data_dir,
            audit,
            proposals,
            settings.whisper_model,
            settings.whisper_model_path,
        )
        index = MarkdownVaultIndex(settings.vault_path, settings.index_path, audit)
        return cls(settings, audit, permissions, proposals, voice, index)
