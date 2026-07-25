# AGENTS.md — repo governance for chat-memory-intelligence

> Read this FIRST, before `.genesis/DONE.html` or `.genesis/PLAN.md` (see `.genesis/KICKOFF.md`
> read order). This file is about **how to work in this repo**; `.genesis/` is about **what to build**.
> `CLAUDE.md` does not exist separately — Claude Code should read this file directly.

## Stack
- Backend: Python, FastAPI
- Storage: PostgreSQL + pgvector (long-term memory), Redis (session cache)
- Orchestration: Temporal (write path + decay job)
- Object storage: S3 (archival)
- LLM/embeddings: any GPT-class provider for extraction/response, an embedding provider for vectors
- Frontend: none yet — deferred (see DONE.html Phase 2 "deferred" table)

## Commands
- Lint + typecheck: `ruff check . && mypy src`
- Tests: `pytest -q`
- Rebuild context graph after `src/` exists: `node <genesis-kit>/tools/graphizer.mjs . --write`

## Conventions
- Every DB query touching memory records must be scoped by `user_id` — no exceptions, no "just this once."
- New modules go under `src/memory/`; tests mirror them under `tests/`.
- Structured LLM outputs (extractor, evaluator) are validated against a schema — never parsed as free text.
- Prefer explicit "I don't know" over a guessed answer when memory retrieval is empty or degraded.

## Hard boundaries (do not cross without updating `.genesis/context-graph.json`)
- No cross-user data leakage.
- A deleted memory must never be retrieved again.
- Memory retrieval failure must never block a chat response (timeout + fallback to no-memory context).
- Every stored memory must carry a `source` (provenance) — no record without one.

## Planning docs (read after this file)
- `.genesis/DONE.html` — locked spec, definition of done, implementation plan (do not edit without being asked)
- `.genesis/PLAN.md` — milestones M1–M9 being executed
- `.genesis/wiki/index.md` — what's already built / researched, read before starting a milestone
- `.genesis/LOOPS.md` — the build/debug/research/verify loop mechanics
