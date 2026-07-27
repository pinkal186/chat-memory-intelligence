# M6 — Economics (iteration 1)

Status: prototype complete

What I implemented:
- `src/memory/cost_tracking.py`: lightweight prototype for recording per-memory and per-operation costs
- Instrumented `src/memory/store.py` to record embedding/storage costs on `add`, record retrieval cost on `query_by_user`, and mark deletes in the cost tracker
- Instrumented `src/memory/retriever.py` to emit a retrieval-level cost event
- Added `tests/test_economics.py` which verifies cost recording and `cost_per_useful_memory()` semantics

Tests:
- Ran `pytest tests/test_economics.py` → 1 passed (with DeprecationWarnings)

Next steps (not done here):
- Integrate cost telemetry with billing exporters (Prometheus/OpenTelemetry/billing pipeline)
- Extend decay job to attribute costs over time and compute per-user/monthly costs
- Add more granular cost categories (embedding per token, retrieval per result)

Files changed:
- src/memory/cost_tracking.py (new)
- src/memory/store.py (instrumentation)
- src/memory/retriever.py (instrumentation)
- tests/test_economics.py (new)

Checkpoint created: M6-iteration-1
