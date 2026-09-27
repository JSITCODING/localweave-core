from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from localweave.app import Services
from localweave.runtime import Settings


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="localweave",
        description="Local-first, approval-gated tools for private Markdown vaults",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create private local configuration")
    init.add_argument("--vault", required=True, type=Path, help="Path to the Markdown vault")
    sub.add_parser("doctor", help="Check configuration and local dependencies")
    sub.add_parser("status", help="Show local configuration and readiness")
    sub.add_parser("index", help="Rebuild the local Markdown search index")

    search = sub.add_parser("search", help="Search the local Markdown index")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=8)

    voice = sub.add_parser("voice", help="Queue and review voice notes")
    voice_sub = voice.add_subparsers(dest="voice_command", required=True)
    voice_sub.add_parser("list", help="List queued voice notes")
    ingest = voice_sub.add_parser("ingest", help="Copy a voice note into the local queue")
    ingest.add_argument("path", type=Path)
    transcribe = voice_sub.add_parser("transcribe", help="Transcribe a queued voice note")
    transcribe.add_argument("voice_id")
    propose = voice_sub.add_parser("propose", help="Create a reviewable vault proposal")
    propose.add_argument("voice_id")
    propose.add_argument("--target", default="Inbox.md")

    proposal = sub.add_parser("proposal", help="Review and apply proposed vault writes")
    proposal_sub = proposal.add_subparsers(dest="proposal_command", required=True)
    proposal_sub.add_parser("list", help="List proposals")
    show = proposal_sub.add_parser("show", help="Show proposal content and diff")
    show.add_argument("proposal_id")
    apply = proposal_sub.add_parser("apply", help="Apply an explicitly approved proposal")
    apply.add_argument("proposal_id")
    apply.add_argument(
        "--approve",
        action="store_true",
        help="Confirm this exact durable vault write",
    )

    audit = sub.add_parser("audit", help="Show recent local audit events")
    audit.add_argument("--limit", type=int, default=20)
    return parser


def _status(services: Services) -> None:
    settings = services.settings
    print("LocalWeave mode: local-only")
    print(f"Repository: {settings.repo_root}")
    print(f"Private config: {settings.config_path}")
    print(f"Markdown vault: {settings.vault_path}")
    print(f"Vault available: {'yes' if settings.vault_path.is_dir() else 'no'}")
    print(f"Local index: {settings.index_path}")
    print(f"Private data: {settings.data_dir}")
    print(f"Private state: {settings.state_dir}")
    print(f"Rebuildable cache: {settings.cache_dir}")
    print(
        "Local speech engine: "
        + (
            services.voice.transcriber.engine() or "not installed (notes remain queued)"
        )
    )
    print("Vault writes: proposal + explicit approval required")


def _doctor(settings: Settings) -> bool:
    checks = [
        ("Private config", settings.config_path.exists(), settings.config_path),
        ("Markdown vault", settings.vault_path.is_dir(), settings.vault_path),
        ("ffmpeg", shutil.which("ffmpeg") is not None, shutil.which("ffmpeg") or "missing"),
        (
            "whisper-cli",
            shutil.which("whisper-cli") is not None,
            shutil.which("whisper-cli") or "missing",
        ),
        (
            "Whisper model",
            bool(settings.whisper_model_path and settings.whisper_model_path.is_file()),
            settings.whisper_model_path or "not configured",
        ),
    ]
    settings.ensure_runtime_dirs()
    runtime_writable = all(
        os.access(path, os.W_OK)
        for path in (settings.data_dir, settings.state_dir, settings.cache_dir)
    )
    checks.append(("Private runtime directories", runtime_writable, settings.data_dir.parent))
    for label, ready, detail in checks:
        print(f"{'OK' if ready else 'MISSING':7} {label}: {detail}")
    return all(ready for _, ready, _ in checks)


def _voice_command(args: argparse.Namespace, services: Services) -> None:
    if args.voice_command == "list":
        items = services.voice.list()
        if not items:
            print("No voice notes are queued.")
            return
        for item in items:
            print(f"{item.id}  {item.status:20}  {item.original_name}")
        return
    if args.voice_command == "ingest":
        item = services.voice.ingest(args.path)
    elif args.voice_command == "transcribe":
        item = services.voice.transcribe(args.voice_id)
    else:
        proposal = services.voice.propose(args.voice_id, args.target)
        print(f"Created proposal {proposal.id} for {proposal.target}")
        print(f"Review it with: localweave proposal show {proposal.id}")
        return
    print(f"Voice item {item.id}: {item.status}")
    if item.error:
        print(item.error)


def _proposal_command(args: argparse.Namespace, services: Services) -> None:
    if args.proposal_command == "list":
        proposals = services.proposals.list()
        if not proposals:
            print("No proposals exist.")
            return
        for proposal in proposals:
            print(f"{proposal.id}  {proposal.status:10}  {proposal.target}")
        return
    proposal = services.proposals.load(args.proposal_id)
    if args.proposal_command == "show":
        print(f"Proposal: {proposal.id}")
        print(f"Status: {proposal.status}")
        print(f"Target: {proposal.target}")
        print(f"Source: {proposal.source}\n")
        print(proposal.content)
        print("\n--- Proposed diff ---")
        print(services.proposals.preview(proposal) or "No content change.")
        return
    if not args.approve:
        print(services.proposals.preview(proposal) or "No content change.")
        raise PermissionError("Re-run with --approve after reviewing this exact diff.")
    target = services.proposals.apply(args.proposal_id, approved=True)
    print(f"Applied proposal {proposal.id} to {target}")


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        settings = Settings.load()
        if args.command == "init":
            path = settings.write_config(args.vault)
            print(f"Created private LocalWeave configuration at {path}")
            print("Next: run 'localweave doctor'.")
            return 0
        if args.command == "doctor":
            return 0 if _doctor(settings) else 1

        services = Services.build(settings)
        if args.command == "status":
            _status(services)
        elif args.command == "index":
            count = services.index.rebuild()
            print(f"Indexed {count} Markdown notes locally.")
        elif args.command == "search":
            results = services.index.search(args.query, args.limit)
            if not results:
                print("No matching Markdown notes found.")
            for result in results:
                print(f"\n{result.title}\n{result.path}\n{result.excerpt}")
        elif args.command == "voice":
            _voice_command(args, services)
        elif args.command == "proposal":
            _proposal_command(args, services)
        elif args.command == "audit":
            for entry in services.audit.tail(args.limit):
                print(json.dumps(entry, ensure_ascii=False))
        return 0
    except (FileNotFoundError, PermissionError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
