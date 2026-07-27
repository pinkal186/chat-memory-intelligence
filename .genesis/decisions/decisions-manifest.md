# decisions-manifest — chat-memory-intelligence
Generated: 2026-07-25 via KICKOFF-INTERVIEW.md (answers derived from memory-system.html design study)

## Trade-off ranking
1. Reliability
2. Maintainability
3. Cost
4. Speed

Rationale (from doc Part IV/4.1): "the system should degrade to slower but correct, never fast but wrong" and
invariants (no cross-user leakage, retrieval failure must not block a response) are treated as non-negotiable
before performance or cost.

## Scale
Launch: single-user / small-team prototype — the 30-Day Stack (Part 2.2): Next.js, FastAPI, Postgres+pgvector,
Temporal, Redis, S3. No dedicated vector cluster yet.
12 months: modeled in doc's capacity-planning example (Part 4.1) — up to ~1M users, 10% active, ~140 memory
writes/sec, ~12M embeddings/day. Architecture should not block this growth path even if not built yet
(exit hatch: swap pgvector for a dedicated vector cluster without redrawing the architecture).

## Project type
Prototype (30-day MVP stack), architected with an explicit growth path to production
(Part III adds observability/security/reliability/infra/governance/economics; Part VI's 5-phase roadmap
sequences the growth).

## Performance constraints (non-negotiable)
- Retrieval latency p95 < 100ms (Part 4.1, SLOs)
- Availability 99.9% (~43 min/month downtime budget)
- Retrieval precision ≥ 90%

## UX / brand constraints
Not specified in the design doc (doc is architecture-focused, not UI-focused). No "must feel like X" reference
given — treat as open, to be decided when a UI is scoped.

## Failure behaviour
Graceful degradation only — memory retrieval is optional. If the memory DB/service is down, the chatbot must
keep answering, just without personalization (Part 3.1, Phase 12 Reliability). Backed by timeouts (~200ms),
circuit breakers, and a fallback path that answers with no memory context.

## Integration points
- LLM provider (GPT-class model) for capture/extraction and response generation
- PostgreSQL + pgvector for long-term memory storage and vector search
- Redis for session-memory cache
- Temporal (or Celery) for write-path/decay-job orchestration
- Embedding provider (e.g. OpenAI text-embedding) for vector generation
- Observability: Prometheus, Grafana, PostHog, Langfuse/OpenTelemetry (deferred until needed)
- Object storage (S3) for archival

## Auth requirements
Tenant isolation is a hard invariant: every query scoped by `user_id`, enforced with Postgres row-level
security so a forgotten filter cannot leak data across users (Part 3.1, Phase 11 Security).

## Compliance constraints
- PII detection filter (e.g. Presidio-style) blocks passwords/card numbers/secrets before they are ever written.
- Encryption at rest for sensitive memory (AES-256, keys in a key manager).
- Data-residency rules noted as a real constraint under GDPR if EU users are in scope (deferred — not yet
  confirmed as in-scope for this project; flag as a known unknown below).

## Primary failure mode (the honest one)
Memory pollution / the "almost right" problem: storing too much noise degrades retrieval, or a wrong memory
(e.g. "thinking of moving" stored as "lives in") gets surfaced with false confidence. The doc calls this the
most common and most expensive failure to get wrong (Part 0.2, Part L5, L8).

## Quality bar ("embarrassed to ship if...")
Shipping a system that leaks one user's memory to another user, or that confidently states a wrong fact about
the user without any way to trace where that belief came from (no provenance).

## Known unknowns → research spikes needed
- Whether this project needs multi-user isolation from day one, or is single-user for now (affects whether
  Phase 11 Security / row-level security is an M1 requirement or deferred).
- Whether GDPR/data-residency applies (depends on whether real user data / EU users are in scope).
- Final UI/UX surface (chat app, browser extension, API-only) — not specified in the design doc.

## Assumptions never stated aloud (agent-inferred from answers above)
- The project is bootstrapping from the design study in [memory-system.html](../../memory-system.html) rather
  than a fresh blank-slate requirement — the architecture in that doc is the intended target design, not just
  reference material.
- "Production system" concerns (Part III/IV) are the long-term target, but M1-M3 will follow the 30-Day Stack
  and 5-phase roadmap (Part 2.2, Part 6.4) rather than jumping straight to full production hardening.
- Single-tenant/single-user is acceptable for the earliest milestone, with tenant isolation added no later
  than the milestone that introduces multi-user support.
