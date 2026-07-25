import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory.sql_store import SQLiteMemoryStore
from memory.schema import MemoryRecord
from memory.retriever import retrieve_for_user


def test_tenant_isolation(tmp_path):
    db = tmp_path / "iso.db"
    store = SQLiteMemoryStore(str(db))

    r = MemoryRecord(user_id="userA", content="private fact")
    store.add(r)

    rows_b = retrieve_for_user(store, "userB")
    assert len(rows_b) == 0
    store.close()
