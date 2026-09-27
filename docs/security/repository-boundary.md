# Repository And Privacy Boundary

A private Git remote is not a privacy control strong enough for LocalWeave. The repository itself must remain publishable without exposing personal content, credentials, machine paths, or derived memory.

## Track In Git

- Source code.
- Synthetic tests.
- Sanitized examples.
- Public-safe documentation.
- Dependency and tooling metadata.
- Architecture decisions and threat-model changes.

## Keep Outside Git

- Markdown vault content or exports.
- Absolute personal paths and usernames.
- Voice recordings and transcripts.
- Journals, conversation history, personal memories, and user profiles.
- Proposals, snapshots, indexes, embeddings, audit history, and session state.
- Model files and offline knowledge datasets.
- API keys, OAuth tokens, cookies, certificates, passwords, and credential exports.
- Downloaded third-party references that are not licensed for redistribution.

## Controls

1. Platform-specific config/data/state/cache directories are outside the checkout.
2. The private config file is owner-readable only.
3. `.gitignore` blocks common private/runtime paths and artifact types.
4. Package metadata supports only tested Python versions and names the public MIT license.
5. Examples and tests use fictional content and temporary directories.
6. Audit events minimize content; searches store fingerprints rather than raw query text.
7. Tool outputs and model prompts must never log secrets by default.

## Before Publishing Or Updating A Remote

Do not assume `.gitignore` proves safety. Before attaching any remote:

1. Review every tracked filename with `git ls-files`.
2. Search tracked text for usernames, home paths, emails, tokens, vault excerpts, and credentials.
3. Run a dedicated secret scanner over the full Git history.
4. Inspect package build contents, not only the working tree.
5. Confirm examples and screenshots are synthetic.
6. Confirm third-party documents have redistribution permission.
7. Document who can access the remote and why.

Remote publication is an explicit approval step. Passing these controls establishes readiness; it does not authorize creating a remote, pushing, or changing visibility.

## Future Credentials

Environment variables are acceptable as process-level injection but are easy to expose through debugging and child processes. High-value credentials should eventually use the operating-system keychain or a dedicated secrets provider. The model should receive capability results, never raw credential values.
