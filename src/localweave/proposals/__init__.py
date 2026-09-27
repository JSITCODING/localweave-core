"""Reviewable and recoverable Markdown-vault write proposals."""

from .models import Proposal
from .service import ProposalStore

__all__ = ["Proposal", "ProposalStore"]
