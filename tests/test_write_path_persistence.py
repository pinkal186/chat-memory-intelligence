import os
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory import extract_memories, evaluate_candidate
from memory.sql_store import SQLiteMemoryStore


def test_sqlite_store_persists_records(tmp_path):
    db = tmp_path / "mem.db"
    store = SQLiteMemoryStore(str(db))

    text = "I use PostgreSQL and I'm building SecondBrainLabs"
    candidates = extract_memories(text, user_id="persist-user")
    for c in candidates:
        if evaluate_candidate(c):
            store.add(c)

    # new connection to verify persistence
    store2 = SQLiteMemoryStore(str(db))
    rows = store2.query_by_user("persist-user")
    assert len(rows) == 2
    for r in rows:
        assert r.content
    store.close()
    store2.close()
