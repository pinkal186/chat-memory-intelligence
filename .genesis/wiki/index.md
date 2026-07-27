# Wiki Index — chat-memory-intelligence

The project knowledge base. Same schema as the agentic-swe-kit wiki: concept pages in `concepts/`,
each with frontmatter and ≥2 `[[wikilinks]]`. The L3 RESEARCH loop writes here; G0 reads here first.

> **Read this file before any milestone (G0 step 1).** Pick candidate pages by name-matching the
> milestone's nouns, then drill in. The wiki is what prevents rebuilding work that already exists.

## Entities (the things this system has)
- [[concepts/Memory-Record]] — the typed record: id, user_id, type, content, importance, confidence, source, created_at, updated_at, weight
- [[concepts/Memory-Store]] — four tiers (working / session / long-term / knowledge), Postgres+pgvector for long-term
- [[concepts/Audit-Log]] — append-only log of every write/read/delete (M5 Governance)
- [[concepts/Golden-Set]] — pinned retrieval test cases used by the eval gate (M2, M7)

## Concepts (how it works)
- [[concepts/Write-Path]] — Extractor → Evaluator (utility score + PII filter) → Memory Store (M1)
- [[concepts/Read-Path]] — Retriever (vector+keyword+graph) → Ranking → Context Composer → Response LLM (M2)
- [[concepts/Decay]] — nightly job: weight = importance × recency × reinforcement, archive below floor (M1/M3)
- [[concepts/Reliability-and-Isolation]] — timeout/circuit-breaker degradation, row-level tenant scoping (M3)
- [[concepts/Observability]] — retrieval rate, correction rate, latency, cost metrics on every write/read (M4)
- [[concepts/Governance]] — audit log, hard-delete guarantee, provenance-based explainability (M5)
- [[concepts/Economics]] — cost per useful memory; write-gate and decay as cost controls (M6)
- [[concepts/CI-CD-for-AI]] — eval gate blocking golden-set regressions, shadow mode for new versions (M7)
- [[concepts/Human-in-the-Loop]] — corrections update existing records, "forget that" hard-deletes (M8)
- [[concepts/Continuous-Learning]] — reflection agent consolidation, conflict resolution on write (M9, v2 shelf)

## Sources (research distilled by L3)
- [[concepts/memory-system-design-study]] — full design study | filed 2026-07-25 | see [memory-system.html](../../memory-system.html)

## Seeded from agentic-swe-kit
Relevant global concept pages for this project's phases (pointers only — read on demand):
- $AGENTIC_SWE_WIKI_ROOT/llmops-ai-agents/concepts/RAG-Architecture.md — retrieval design, hybrid search (M2)
- $AGENTIC_SWE_WIKI_ROOT/llmops-ai-agents/concepts/Agent-Fundamentals.md — extractor/evaluator agent design (M1)
- $AGENTIC_SWE_WIKI_ROOT/llmops-ai-agents/concepts/Evaluation-Frameworks.md — golden-set precision/recall for retrieval (M2, M7)
- $AGENTIC_SWE_WIKI_ROOT/llmops-ai-agents/concepts/Observability-and-Cost-Control.md — retrieval rate, correction rate, cost/useful-memory (M4, M6)
- $AGENTIC_SWE_WIKI_ROOT/llmops-ai-agents/concepts/Production-Hardening.md — graceful degradation when memory is unavailable (M3)
- $AGENTIC_SWE_WIKI_ROOT/designing-data-intensive-applications/concepts/Storage-Engines.md — Postgres+pgvector as the storage spine (M1)
- $AGENTIC_SWE_WIKI_ROOT/designing-data-intensive-applications/concepts/Conflict-Resolution.md — merging contradictory memories (M9, v2 shelf)
- $AGENTIC_SWE_WIKI_ROOT/designing-data-intensive-applications/concepts/Partitioning-Strategies.md — scaling the memory store past MVP
- $AGENTIC_SWE_WIKI_ROOT/security-engineering/concepts/Access-Control.md — tenant isolation / row-level security (invariant: no cross-user leakage, M3)
- $AGENTIC_SWE_WIKI_ROOT/security-engineering/concepts/Privacy-and-Inference-Control.md — PII filtering before write, governance/deletion (M1, M5)
- $AGENTIC_SWE_WIKI_ROOT/security-engineering/concepts/Threat-Modeling.md — trust boundary work once multi-user is in scope (M3)
- $AGENTIC_SWE_WIKI_ROOT/security-engineering/concepts/Audit-Logging.md — append-only audit trail patterns (M5)
