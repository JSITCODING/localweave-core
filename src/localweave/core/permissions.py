from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PermissionTier(StrEnum):
    READ_ONLY = "read-only"
    ASK_FIRST = "ask-first"
    RESTRICTED = "restricted"
    PROHIBITED = "prohibited-by-default"


class Action(StrEnum):
    READ_VAULT = "read_vault"
    INDEX_VAULT = "index_vault"
    TRANSCRIBE_LOCAL = "transcribe_local"
    CREATE_PROPOSAL = "create_proposal"
    WRITE_VAULT = "write_vault"
    RUN_UNRESTRICTED_SHELL = "run_unrestricted_shell"


@dataclass(frozen=True)
class PermissionDecision:
    action: Action
    tier: PermissionTier
    allowed: bool
    approval_required: bool
    reason: str


class PermissionEngine:
    _TIERS = {
        Action.READ_VAULT: PermissionTier.READ_ONLY,
        Action.INDEX_VAULT: PermissionTier.READ_ONLY,
        Action.TRANSCRIBE_LOCAL: PermissionTier.READ_ONLY,
        Action.CREATE_PROPOSAL: PermissionTier.READ_ONLY,
        Action.WRITE_VAULT: PermissionTier.ASK_FIRST,
        Action.RUN_UNRESTRICTED_SHELL: PermissionTier.PROHIBITED,
    }

    def evaluate(self, action: Action, approved: bool = False) -> PermissionDecision:
        tier = self._TIERS[action]
        if tier is PermissionTier.PROHIBITED:
            return PermissionDecision(action, tier, False, False, "Action is prohibited.")
        if tier is PermissionTier.ASK_FIRST and not approved:
            return PermissionDecision(
                action, tier, False, True, "Explicit approval is required."
            )
        return PermissionDecision(action, tier, True, False, "Action is allowed.")
