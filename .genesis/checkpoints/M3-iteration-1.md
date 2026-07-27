# M3 — iteration 1

- date: 2026-07-25
- milestone: M3 — Reliability + tenant isolation invariants
- iteration: 1
- author: automation (GitHub Copilot agent)

## Summary
Completed M3 verification: `tests/test_reliability.py` and `tests/test_isolation.py` passed.

## Actions performed
- Reviewed `src/memory/sql_store.py`, `src/memory/store.py`, and `src/memory/retriever.py`.
- Confirmed `retrieve_for_user` degrades gracefully on store failure.
- Confirmed tenant isolation via `SQLiteMemoryStore.query_by_user` and `MemoryStore.query_by_user`.
- Ran demo tests and confirmed expected behavior.
- Updated `.genesis/checkpoints/CURRENT.md` to record M3 prototype and progress.

## Demo command
```
pytest tests/test_reliability.py tests/test_isolation.py -q
```

## Next steps
- Implement full DB integration (docker-compose with Postgres+pgvector + SQLAlchemy or psycopg) and run integration tests.
- Harden reliability (timeouts, circuit breaker, chaos tests) as part of M3 iteration 2.
