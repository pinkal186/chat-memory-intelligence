import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory.sql_store import SQLiteMemoryStore
from memory import MemoryRecord


def test_no_cross_user_leakage(tmp_path):
    db = tmp_path / "inv.db"
    store = SQLiteMemoryStore(str(db))

    r = MemoryRecord(user_id="userA", content="I use Postgres")
    store.add(r)

    rows_b = store.query_by_user("userB")
    assert len(rows_b) == 0
    store.close()


def test_deleted_never_retrieved(tmp_path):
    db = tmp_path / "inv2.db"
    store = SQLiteMemoryStore(str(db))

    r = MemoryRecord(user_id="deleter", content="temporary fact")
    store.add(r)
    rows = store.query_by_user("deleter")
    assert len(rows) == 1

    # delete and verify
    store.delete_by_id(r.id)
    rows_after = store.query_by_user("deleter")
    assert len(rows_after) == 0
    store.close()
