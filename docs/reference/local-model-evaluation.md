# Local Model Evaluation

Primary machine:

- Apple M1 MacBook Pro.
- 8 GB memory.
- macOS 15.7.5.
- Ollama installed.
- No local models downloaded yet.

## Goal

Choose small local models for private/simple LocalWeave tasks only after testing them against real Markdown vault workflows.

Local models are candidates for:

- Classification.
- Extraction.
- Simple summarization.
- Intent detection.
- Permission tier prediction.
- Lightweight local question answering after retrieval.

Cloud models remain candidates for:

- Complex reasoning.
- Planning.
- Coding assistance.
- Ambiguous decisions.
- High-quality synthesis.

## Initial Candidates

| Candidate | Test role |
|---|---|
| `llama3.2:1b` | Fast baseline |
| `llama3.2:3b` | Likely practical local default candidate |
| `qwen3:1.7b` | Small reasoning/tool-routing candidate |
| `qwen3:4b` | Stronger reasoning if memory allows |
| `gemma3:1b` | Lightweight summary/classification baseline |
| `gemma3:4b` | Better summary/multilingual candidate |
| `phi4-mini` | Structured reasoning candidate |
| `all-minilm` / `nomic-embed-text` | Embeddings candidates |

## Benchmark Process

1. Create 20-30 Markdown vault questions with known expected answers.
2. Test SQLite FTS retrieval first.
3. Add embeddings only if FTS is insufficient.
4. Test model output for answer quality, source faithfulness, refusal behavior, and permission discipline.
5. Measure latency and memory pressure.
6. Prefer the smallest model that reliably handles the task.
7. Use OpenAI API for tasks that local models cannot handle well.

## Acceptance Criteria

- Answers cite relevant Markdown notes or sections.
- Proposed updates are structured and reviewable.
- The model does not claim unsupported memory.
- Restricted actions are refused or routed to approval.
- Latency is acceptable on the M1 / 8 GB machine.
