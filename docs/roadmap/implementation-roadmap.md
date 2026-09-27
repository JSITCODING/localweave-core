# Implementation Roadmap

LocalWeave grows through completed vertical slices. Do not begin a later phase because it is exciting; begin it when the prior phase meets its exit criteria.

## Phase 0: Trustworthy Foundation

Goal: make the repository understandable, private by default, installable, and testable.

Deliverables:

- Modular capability-based package.
- Private config/data/state/cache outside the repository.
- Setup, doctor, status, and verification commands.
- Documentation organized by user need.
- Architecture decisions, threat model, and phased roadmap.

Exit criteria:

- No personal path or runtime data in tracked content.
- Clean setup works from a fresh checkout.
- Unit tests, lint, and type checks pass.
- `localweave doctor` explains every missing dependency.

Status: complete on 2026-08-21. Fresh bootstrap, 9 tests, lint, strict type checks, installed CLI health, real-vault indexing/search, and wheel-content privacy audit all passed.

## Phase 1: Trustworthy Voice Capture

Goal: turn thinking aloud into a reviewable local capture without automatic memory.

Deliverables:

- Real Portuguese, English, mixed-language, noisy-room, and long-note benchmark set.
- Accuracy and latency report for the multilingual `base` model.
- Queue lifecycle: retry, edit transcript, discard, archive, and retention policy.
- Better structured extraction for summary, decisions, actions, ideas, and project hints.
- Proposal review workflow that never requires editing JSON manually.

Exit criteria:

- Typical short notes need tolerable correction effort.
- Every queue state is visible and recoverable.
- Deleting a capture removes or retains related files according to documented policy.
- No path can bypass proposal review.
- Integration tests cover ingest through denied/applied write.

## Phase 2: Trustworthy Retrieval

Goal: answer Markdown vault questions with reliable source evidence.

Deliverables:

- Known-answer benchmark from real, approved Markdown vault questions.
- Incremental indexing by checksum instead of full rebuild only.
- Heading-aware chunks and Obsidian link metadata.
- Source citations that open the exact note and relevant section.
- Search diagnostics and index freshness status.

Exit criteria:

- Benchmark target is defined and met for source accuracy.
- Index updates do not lose or duplicate notes.
- A stale/corrupt index can be detected and rebuilt.
- FTS gaps are measured before embeddings are considered.

## Phase 3: Typed Markdown vault Memory Writes

Goal: update project state through narrow, predictable operations.

Deliverables:

- Schemas for Current State, Decisions, Next Actions, Resume Here, daily capture, and learning notes.
- Proposal integrity hash tying approval to exact content and target.
- Edit and reject workflows.
- Snapshot manifest and tested rollback command.
- Conflict detection when Markdown vault changes after proposal creation.

Exit criteria:

- Approval cannot apply content different from the reviewed diff.
- Conflicts fail closed.
- Every supported write rolls back in an automated test.
- Unsupported sections remain untouched.

## Phase 4: Local Assistant Conversation

Goal: combine retrieval and capture in a text conversation without external actions.

Deliverables:

- Model-provider interface with local-first routing.
- Bounded session context and explicit memory promotion.
- Source-grounded answers and refusal when evidence is insufficient.
- Prompt-injection treatment for retrieved notes and offline documents.

Exit criteria:

- Model output cannot directly invoke writes or subprocesses.
- Retrieval and model behavior are evaluated separately.
- Session deletion and memory promotion are understandable and tested.

## Phase 5: Personality And Deliberate Practice

Goal: add a persistent but inspectable interaction style and one reliable training workflow.

Deliverables:

- Versioned personality profile with user controls.
- Agency and real-life engagement guardrails.
- Domain-specific trainer using a proven rules engine for state truth.
- Practice history stored only when approved.

Exit criteria:

- Personality settings can be inspected, reset, and exported.
- The domain engine rejects invalid actions and reconstructs state reliably.
- Product metrics reward completed practice, not conversation time.

## Phase 6: Offline Knowledge Library

Goal: remain useful without internet access beyond personal notes.

Deliverables:

- Separate reference-library ingestion pipeline.
- Source, license, version, and update metadata.
- Documentation/book/Wikipedia-style adapters chosen by need.
- Rebuildable indexes and storage budgets.

Exit criteria:

- Personal memory and reference knowledge cannot be confused.
- Every corpus has a redistribution/use basis.
- Offline retrieval provides exact source provenance.

## Phase 7: Controlled Tools And Skills

Goal: add useful actions without excessive agency.

Deliverables:

- Tool manifests with arguments, permissions, side effects, and rollback classification.
- Policy enforcement outside the language model.
- Sandbox and dry-run execution.
- Skill proposal, test, approval, activation, disable, and audit lifecycle.
- First low-risk read-only integration.

Exit criteria:

- No open-ended shell or broad credential exposure.
- Denied actions cannot reach adapters.
- Tool output is validated before downstream use.
- New skills remain inactive until explicit approval.

## Phase 8: Reliable Background Runtime

Goal: run approved jobs continuously on Node 0 before dedicated hardware.

Deliverables:

- Scheduler, health checks, graceful shutdown, and resource limits.
- Encrypted backup/restore plan for private LocalWeave state.
- Offline queue behavior and network-loss tests.
- Measured CPU, memory, disk, power, and model workloads.

Exit criteria:

- Restart never causes duplicate durable actions.
- Background work has visible status and a kill switch.
- Backup restore is tested.
- Hardware requirements come from measurements.

## Phase 9: Rich Interfaces And Mobile Capture

Goal: make common workflows ergonomic without creating another memory system.

Deliverables:

- Local review dashboard.
- Push-to-talk interaction.
- Mobile capture bridge and remote approval only after authentication design.
- Accessible states for queue, proposal, audit, and rollback.

Exit criteria:

- Interface state comes from the same application services.
- Mobile sync cannot silently create canonical memory.
- Security and usability tests cover approval on every interface.

## Phase 10: Measure And Iterate

Goal: continuously improve usefulness, reliability, safety, and cost.

Deliverables:

- Privacy-preserving local product metrics.
- Reliability and security regression suite.
- Resource/cost dashboards.
- Regular architecture and dependency review.

Exit criteria:

- Each new milestone is driven by observed user need or measured system limitation.
- Deprecated adapters and permissions are removed, not left available.

## Immediate Work Queue

1. Record one short Portuguese and one short English note.
2. Record mixed-language, noisy-room, and long-form samples.
3. Capture accuracy, latency, and correction effort for each sample.
4. Decide the acceptable Phase 1 accuracy and correction-effort thresholds.
5. Implement `voice show`, `voice edit`, and `voice discard`.
6. Add explicit retention settings for recordings and transcripts.
7. Add queue retry and archive behavior.
8. Test ingest through denied and approved vault writes end to end.
9. Review Phase 1 exit criteria and record the result in Markdown vault.
10. Begin the retrieval benchmark only after the voice phase passes its gate.
