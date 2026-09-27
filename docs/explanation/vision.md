# LocalWeave Agent OS Vision

LocalWeave should become a persistent personal agent OS layered over Markdown vault, not a normal stateless assistant.

The operating idea:

```text
Markdown vault = durable human-readable source of truth.
LocalWeave = persistent reasoning, memory, interface, and tool-control layer.
```

## Design Boundary

LocalWeave should expand the user's ability to live, learn, build, train, reflect, and execute. It must not become the center of life.

Companion behavior is allowed, but bounded:

- LocalWeave can have a stable personality and communication style.
- LocalWeave can remember preferences, projects, recurring struggles, and training goals when approved.
- LocalWeave can challenge, coach, remind, and practice with the user.
- LocalWeave should encourage real-world action, reflection, work, and learning.
- LocalWeave must not optimize for dependency, endless conversation, isolation, or replacing human relationships.

## Interface Layers

Initial interface:

- Text CLI.
- Voice-note ingestion and review queue.
- Markdown vault retrieval and source-linked answers.
- Reviewable proposed updates.

Later interface layers:

- Conversational voice mode.
- Mobile capture.
- Desktop companion panel.
- Background worker for approved jobs.
- Optional local dashboard.

Voice note ingestion should be treated as a Markdown vault capture pipeline:

```text
Voice note
  -> transcription
  -> classification
  -> summary / extracted decisions / tasks / ideas
  -> review queue
  -> approved Markdown vault update
```

Voice input should not automatically become durable memory. LocalWeave should ask before saving reflections, decisions, project changes, or personal history.

## Autonomous Skill Acquisition

LocalWeave may eventually gain new skills, but only through controlled acquisition.

Allowed future flow:

```text
Need detected
  -> skill proposal
  -> permission and risk classification
  -> sandboxed install or generated adapter
  -> tests / dry run
  -> user approval
  -> activation
  -> audit log
```

Autonomous skill acquisition must not mean unrestricted shell access, silent package installation, broad OAuth grants, or hidden background behavior.

Examples of possible skills:

- Markdown vault summarizer.
- Project handoff updater.
- GitHub issue/PR reader.
- Calendar planning assistant.
- Voice note classifier.
- Domain-specific practice tools backed by deterministic engines.
- Offline knowledge retriever.
- Training analysis adapter.

## Learning and Training Examples

LocalWeave should support deliberate practice, not just passive answers.

Examples:

- Structured practice: a domain engine validates state and rules while LocalWeave provides instruction and explanation.
- Programming practice: LocalWeave asks exercises, checks reasoning, references local docs/books, and keeps a learning history.
- Research review: LocalWeave retrieves offline knowledge, compares sources, and records decisions.
- Data review: LocalWeave analyzes only explicitly selected local exports and proposes concise summaries for review.

When a task has a reliable domain engine, use the engine for truth and use the language model for instruction, explanation, and conversation.

## Personality Layer

The personality should be a persistent configuration and experience layer, not only a single prompt.

Possible configurable dimensions:

- Directness.
- Humor.
- Proactivity.
- Formality.
- Challenge level.
- Talkativeness.
- Independence.

Some behavior may be learned from experience, but it should remain inspectable and adjustable. The system should avoid pretending that learned behavior proves consciousness or moral status.

## Offline Knowledge Library

LocalWeave should assume the internet can disappear.

Long-term target:

- Local Markdown vault.
- Local documentation mirrors for programming tools.
- Local books and reference material where legally owned or freely licensed.
- Local Wikipedia or selected offline encyclopedic datasets if storage allows.
- Local retrieval index over the offline library.

Offline knowledge should be separated from Markdown vault. Markdown vault stores personal memory and decisions; the offline library stores reference material.

## Non-Goals

These are explicitly not first-phase goals:

- Always-on microphone.
- Autonomous control of finances.
- Silent Markdown vault rewriting.
- Unrestricted shell.
- Secret access by the model.
- Replacing real-life goals, relationships, or purpose.
