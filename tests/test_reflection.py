import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory.store import MemoryStore
from memory.schema import MemoryRecord

from memory.reflection import consolidate_scattered_facts


def test_reflection_consolidates_scattered_facts():
    store = MemoryStore()
    r1 = MemoryRecord(user_id="u1", content="uses Postgres", importance=0.2, confidence=0.6)
    r2 = MemoryRecord(user_id="u1", content="uses pgvector", importance=0.1, confidence=0.7)
    r3 = MemoryRecord(user_id="u1", content="deploys with Docker", importance=0.3, confidence=0.8)
    store.add(r1)
    store.add(r2)
    store.add(r3)

    summary = consolidate_scattered_facts(store, "u1")
    assert summary is not None
    rows = store.query_by_user("u1")
    # originals should have been consolidated (deleted) and a single summary exists
    assert len(rows) == 1
    assert "Postgres" in rows[0].content
    assert "pgvector" in rows[0].content
    assert "Docker" in rows[0].content
