# LLM Project Checklist

Load this file when the project involves LLMs (chat, retrieval,
generation, agents, prompt-driven flows). The main `SKILL.md` does not
require these — they only apply when the project is LLM-shaped.

## Mandatory Specs

When LLMs are in scope, generate at least:

- `.trellis/spec/llm/llm-spec.md`
- `.trellis/spec/prompt/prompt-spec.md`

Each must define the items below as concrete contracts, not aspirations.

## Provider And Auth

- [ ] Model provider abstraction (interface, not a hardcoded SDK call site)
- [ ] Supported providers and model IDs declared in one place
- [ ] API key loaded from environment, never committed
- [ ] No private LLM keys exposed to frontend code or shipped binaries
- [ ] Per-environment key separation (dev / staging / prod)
- [ ] Rate-limit handling and quota reporting

## Prompts

- [ ] Prompt templates stored as files, not inline strings scattered across
      the codebase
- [ ] Template inputs typed and validated before render
- [ ] System / user / tool messages clearly separated
- [ ] Versioning policy for prompt changes (filename, hash, or git tag)
- [ ] Prompt diffs reviewable in PRs (no minified or one-line prompts)

## Retrieval (when applicable)

- [ ] Index source defined (DB / vector store / file system)
- [ ] Chunking strategy and chunk size specified
- [ ] Embedding model and dimension declared
- [ ] Query path latency target (p50 / p95)
- [ ] Cache layer rules (key, TTL, invalidation)
- [ ] Re-indexing trigger documented

## Behavior Guardrails

- [ ] Fallback behavior when the model returns nothing useful
- [ ] Hallucination guardrails (grounding requirement, citation rule,
      "I don't know" path)
- [ ] Refusal behavior for off-scope or unsafe requests
- [ ] Maximum output length and truncation policy
- [ ] Tool-use safety (which tools, which arguments validated)

## Reliability

- [ ] Timeout per call (with explicit number, not "reasonable")
- [ ] Retry policy (count, backoff, idempotency check)
- [ ] Partial failure handling (one of N providers down)
- [ ] Circuit-breaker or degrade-gracefully path

## Observability

- [ ] Request/response logging policy (PII redaction included)
- [ ] Token usage logged per call and per session
- [ ] Latency tracked per call
- [ ] Error categories enumerated and counted
- [ ] Sampled prompts captured for offline review

## Evaluation

- [ ] Golden evaluation set committed (inputs + expected behavior)
- [ ] Automated evaluation script with a verification command
- [ ] Regression threshold defined (which metric, what number)
- [ ] Manual review cadence for sampled traffic

## Tests

- [ ] Unit tests for prompt rendering
- [ ] Mocked provider tests for happy path and error path
- [ ] Live smoke test that runs against a real provider in CI when keys
      are available (skipped otherwise, never failed silently)

If a project ships any of these as TODO, mark them in
`docs/REQUIREMENTS_ANSWERS.md` with `(default assumption)` so Codex
knows they are gaps.
