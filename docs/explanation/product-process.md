# Product Process

The Roadmap.sh Product Design roadmap is useful for sequencing product work, but it is not a software architecture. LocalWeave combines its product loop with secure engineering and agent-safety controls.

## Adapted Product Loop

1. Define success: vision, user outcome, constraints, and measurable exit criteria.
2. Discover: observe real workflows, especially voice capture and Markdown vault retrieval.
3. Define: frame one narrow problem and prioritize it against safety and value.
4. Plan: identify assumptions, technical constraints, risk, and the smallest vertical slice.
5. Design the experience: map the user flow, states, errors, approvals, and recovery.
6. Validate: test functionality, usability, privacy, accessibility, and failure cases.
7. Work with engineering: specify boundaries, data contracts, edge cases, and readiness checks.
8. Ship and scale: stabilize one local workflow before adding platforms or background services.
9. Measure and iterate: compare real outcomes to success metrics and revise.

## LocalWeave Design Principles

- Functionality before polish.
- User agency before autonomous convenience.
- Reviewable state before hidden memory.
- Local capability before network dependence.
- Narrow tools before general computer control.
- Reliable domain engines before language-model improvisation.
- Iteration before speculative scale.
- Real-life outcomes before engagement time.

## Success Metrics By Stage

- Capture: transcription accuracy, correction effort, capture completion rate, and zero unapproved writes.
- Retrieval: known-answer accuracy, source-path accuracy, index time, and query latency.
- Memory writes: proposal acceptance rate, rollback success, and schema correctness.
- Agent tools: denied-action correctness, approval clarity, adapter failure containment, and complete audit coverage.
- Companion/training: completed offline actions and practice consistency, never conversation duration.

## Evidence Sources

- Roadmap.sh Product Design roadmap: defining success, discovery, problem framing, risk, user flows, validation, engineering constraints, launch readiness, scaling, and continuous improvement.
- Python Packaging User Guide: `src` layout, `pyproject.toml`, installable CLI, and private package classifier.
- Diátaxis: tutorials, how-to guides, reference, and explanation as separate documentation needs.
- OWASP GenAI/LLM guidance: prompt injection, improper output handling, sensitive disclosure, and excessive agency.
- OWASP Secrets Management: do not hardcode or commit credentials; minimize and audit access.
- NIST SSDF: document security requirements and design decisions; protect source and development artifacts; test and respond continuously.
- XDG Base Directory Specification: separate user configuration, data, state, cache, and runtime files.

The research reference PDF is stored in private LocalWeave application data and is intentionally absent from the repository.
