# PLAN — chat-memory-intelligence

The machine-parseable implementation plan. Mirrors the milestone table in `DONE.html` (DONE.html is the
human/visual view; this is the one loops read). Sliced so each milestone ships in one L1 BUILD pass.

> Slicing rule: a milestone must have (a) a single clear outcome, (b) an exact **demo command** that
> proves it, and (c) a freeze boundary of files it may touch. If you can't write the demo command,
> the milestone is too vague — split it.

---

## Brainstorm (G0.5 — fill before slicing milestones)

> Three fundamentally different approaches to the cognitive job. Pick one. Record the rationale.
> This is the cheapest design decision — you haven't written a line of code yet.

### Approach A — Single-orchestrator MVP, LLM-judge evaluator
One FastAPI service, one Postgres+pgvector database, no message queue. Extraction, evaluation
(LLM-judge scoring utility 1-10), retrieval, and ranking all run in-process, synchronously, on the
30-Day Stack from the design study (memory-system.html §2.2).
- Strengths: fastest to a working write→read loop; matches the "prototype first" project type; minimal
  moving parts to debug.
- Weaknesses: LLM-judge evaluator is non-deterministic (same input can score differently) and gets
  expensive at volume; no queue means a slow extraction blocks the request path until M3 hardens it.

### Approach B — Six-subsystem microservices from day one
Split Capture / Storage / Retrieval / Evaluation / Decay / Governance into separate services from the
start, wired through Temporal, with a deterministic classifier (not an LLM) for evaluation, per the full
production architecture (memory-system.html §L3, §3.1).
- Strengths: matches the eventual production target exactly; no later rewrite of service boundaries;
  deterministic evaluator is consistent and cheap at scale.
- Weaknesses: large upfront build cost before anything is provably useful; over-engineered for a
  single-engineer prototype (violates the doc's own Conway's-law caution, §5.1); nothing to demo for
  several sprints.

### Approach C — In-process library, no service boundary
Memory logic lives as a plain importable module (no HTTP API), synchronous calls, SQLite or local
Postgres, called directly by whatever chat app embeds it.
- Strengths: cheapest and fastest possible way to validate the write-gate/retrieval idea in isolation;
  trivial to unit test.
- Weaknesses: no path to multi-user isolation or async decay/reflection without a near-total rewrite;
  doesn't exercise the reliability/degradation behavior that's a stated invariant.

### Chosen: Approach A — Single-orchestrator MVP, LLM-judge evaluator
Matches the decisions-manifest project type (prototype, growing into production per the 5-phase
roadmap) and gets the core write/read loop working fastest. The exit hatch is already designed in the
source doc: swap the LLM-judge for a deterministic classifier, and split services later, without
redrawing the architecture (memory-system.html §5.1, "Exit strategy"). Reliability and tenant-isolation
invariants are still pulled into M3 early rather than deferred indefinitely, since the doc calls those
non-negotiable regardless of MVP status.

---

## Milestones

### M1 — Memory write path (schema, extractor, evaluator, store)
- **Outcome:** A conversation turn goes in; a structured memory record (with importance, confidence,
  source) comes out the other side in Postgres, or is correctly dropped as low-utility.
- **Phase (swe-master):** 0 Cognitive Design / 6 Memory Architecture
- **Files / freeze boundary:** `src/memory/schema.py`, `src/memory/extractor.py`, `src/memory/evaluator.py`, `src/memory/store.py`, `tests/test_write_path.py`
- **Demo command:** `pytest tests/test_write_path.py -q`
- **Success criteria:** Given "I use PostgreSQL and I'm building SecondBrainLabs" the store contains
  2 records with importance/confidence/source set; given "I had coffee today" no record is written.
- **Loops:** L1, L4
- **Skills:** canon + tdd + data-systems-engineering
- **Token budget:** 50000

### M2 — Memory read path (retrieval, ranking, context composer)
- **Outcome:** Given a query against a seeded store, the top-k memories returned are ranked by the
  documented signal blend (semantic 0.4, recency 0.2, frequency 0.2, importance 0.2) and assembled
  into a context block.
- **Phase:** 6 Memory Architecture / 9 Evaluation Systems
- **Files:** `src/memory/retriever.py`, `src/memory/ranking.py`, `src/memory/context_composer.py`, `tests/test_read_path.py`
- **Demo command:** `pytest tests/test_read_path.py -q`
- **Success criteria:** The "help me design a course" query (memory-system.html §L6 worked example)
  returns the 3 high-relevance memories ahead of the 2 low-relevance ones in the golden-set test.
- **Loops:** L1, L3 (research), L4
- **Skills:** canon + tdd + llmops-ai-agents
- **Token budget:** 50000

### M3 — Reliability + tenant isolation (the non-negotiable invariants)
- **Outcome:** Memory-store failure degrades to an answer without memory instead of an exception;
  user A's query never returns user B's memories.
- **Phase:** 11 Security / 12 Reliability
- **Files:** `src/memory/store.py`, `src/memory/retriever.py`, `tests/test_reliability.py`, `tests/test_isolation.py`
- **Demo command:** `pytest tests/test_reliability.py tests/test_isolation.py -q`
- **Success criteria:** Simulated store outage still returns a 200 response (no memory context, flagged
  degraded); a retrieval for user B run against a store seeded only with user A's memories returns zero
  rows.
- **Loops:** L1, L2 (debug), L4
- **Skills:** canon + tdd + security-engineering + distributed-systems
- **Token budget:** 50000

### M4 — Observability plane (retrieval rate, correction rate, latency, cost)
- **Outcome:** Every write and retrieval emits metrics for retrieval rate, correction rate, latency,
  and cost, visible on a dashboard, matching the four measures in memory-system.html §3.1 Phase 10.
- **Phase:** 10 Observability
- **Files:** `src/memory/metrics.py`, `src/memory/tracing.py`, `tests/test_observability.py`
- **Demo command:** `pytest tests/test_observability.py -q`
- **Success criteria:** A write and a retrieval each emit a metric event with latency and cost fields;
  a retrieval marked "corrected" by a user increments the correction-rate counter.
- **Loops:** L1, L4
- **Skills:** canon + tdd + production-readiness
- **Token budget:** 50000

### M5 — Governance (audit log, deletion, explainability)
- **Outcome:** Every write/read/delete is recorded in an append-only audit log; a deleted memory is
  never retrieved again; "why do you think that" resolves to the record's `source` field
  (memory-system.html §3.1 Phase 15).
- **Phase:** 15 Governance & Compliance
- **Files:** `src/memory/audit_log.py`, `src/memory/governance.py`, `tests/test_governance.py`
- **Demo command:** `pytest tests/test_governance.py -q`
- **Success criteria:** Deleting a memory writes an audit row and the retriever returns zero rows for
  it afterward; a provenance query for any stored memory resolves to a conversation/document/user id.
- **Loops:** L1, L4
- **Skills:** canon + tdd + security-engineering
- **Token budget:** 50000

### M6 — Economics (cost-per-useful-memory tracking)
- **Outcome:** Cost is tracked per useful memory (not raw count); the write-gate (evaluator) and decay
  job are measurable as cost controls, per the worked example in memory-system.html §3.1 Phase 16.
- **Phase:** 16 Economics
- **Files:** `src/memory/cost_tracking.py`, `tests/test_economics.py`
- **Demo command:** `pytest tests/test_economics.py -q`
- **Success criteria:** Given a batch of writes, the cost report separates $/embedding, $/retrieval,
  and $/useful-memory (post-evaluator, post-decay), and dropped/decayed memories are excluded from the
  useful-memory denominator.
- **Loops:** L1, L4
- **Skills:** canon + tdd + data-systems-engineering
- **Token budget:** 50000

### M7 — CI/CD for AI (eval gate, shadow mode)
- **Outcome:** A change that regresses the golden-set retrieval score is blocked before merge; a new
  extractor/ranking version can run in shadow mode alongside the old one for comparison
  (memory-system.html §3.1 Phase 18).
- **Phase:** 18 CI/CD for AI
- **Files:** `src/memory/eval_gate.py`, `tests/golden_set.json`, `tests/test_eval_gate.py`, `.github/workflows/eval-gate.yml`
- **Demo command:** `pytest tests/test_eval_gate.py -q`
- **Success criteria:** Running the eval gate against a deliberately-regressed ranking config fails the
  build; running it against the current config passes; shadow mode runs both versions and diffs results
  without affecting the live response.
- **Loops:** L1, L3 (research), L4
- **Skills:** canon + tdd + llmops-ai-agents
- **Token budget:** 50000

### M8 — Human-in-the-loop (corrections, forget command)
- **Outcome:** A user correction ("no, I moved") updates the relevant memory instead of creating a
  conflicting duplicate; an explicit "forget that" deletes the memory (memory-system.html §3.1 Phase 19).
- **Phase:** 19 Human-in-the-Loop
- **Files:** `src/memory/corrections.py`, `src/memory/forget.py`, `tests/test_hitl.py`
- **Demo command:** `pytest tests/test_hitl.py -q`
- **Success criteria:** Correcting "works in EdTech" to "runs a B2B SaaS" updates confidence/content on
  the existing record (not a new row); "forget that I mentioned Kashmir" deletes the matching memory and
  it is never retrieved again (ties into M3's deleted-never-retrieved invariant).
- **Loops:** L1, L4
- **Skills:** canon + tdd + llmops-ai-agents
- **Token budget:** 50000

### M9 — Continuous learning (reflection agent, conflict resolution) — v2 shelf
- **Outcome:** A scheduled reflection agent consolidates scattered memories into fewer, higher-level
  ones; a conflict check resolves contradictions between old and new memories on write
  (memory-system.html §2.3 "v2 shelf", §6.3 Orchestrator Evolution, §6.4 Phase 3/5).
- **Phase:** 20 Continuous Learning
- **Files:** `src/memory/reflection.py`, `src/memory/conflict_resolution.py`, `tests/test_reflection.py`
- **Demo command:** `pytest tests/test_reflection.py -q`
- **Success criteria:** Three scattered facts ("uses Postgres," "uses pgvector," "deploys with Docker")
  consolidate into one summary memory with the originals archived (not deleted); a new memory that
  contradicts an existing one is either merged, kept as both, or archived with newer/higher-confidence
  winning, per memory-system.html §2.3 "Conflict resolution."
- **Loops:** L1, L3 (research), L4
- **Skills:** canon + tdd + llmops-ai-agents
- **Token budget:** 50000

---

## Progress (loops append here on milestone completion — newest last)

- M1 — Memory write path: completed (tests `tests/test_write_path.py` passed). — 2026-07-25
- M2 — Memory read path: completed (tests `tests/test_read_path.py` passed). — 2026-07-25
- M3 — Reliability & tenant isolation: completed (tests `tests/test_reliability.py` and `tests/test_isolation.py` passed). — 2026-07-25
 - M4 — Observability plane: completed (tests `tests/test_observability.py` passed). — 2026-07-25
- M5 — Governance (audit log, deletion, explainability): completed (tests `tests/test_governance.py` passed). — 2026-07-25
- M6 — Economics (cost-per-useful-memory): completed (tests `tests/test_economics.py` passed). — 2026-07-25
- M7 — CI/CD for AI (eval gate, shadow mode): completed (tests `tests/test_eval_gate.py` passed). — 2026-07-25
- M8 — Human-in-the-loop (corrections, forget command): completed (tests `tests/test_hitl.py` passed). — 2026-07-25
- M9 — Continuous learning (reflection, conflict resolution): completed (tests `tests/test_reflection.py` passed). — 2026-07-25

