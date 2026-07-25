import os
import sys
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory.audit_log import reset, find_events
from memory.sql_store import SQLiteMemoryStore
from memory.schema import MemoryRecord
from memory.retriever import retrieve_for_user
from memory.governance import get_provenance_from_events


def test_audit_log_and_deletion(tmp_path):
    reset()
    db = tmp_path / "gov.db"
    store = SQLiteMemoryStore(str(db))

    r = MemoryRecord(user_id="userA", content="sensitive", source="conv:123")
    store.add(r)

    # audit log should contain a write event
    writes = find_events(event_type="write", memory_id=r.id)
    assert len(writes) == 1

    # provenance should be readable from audit events
    prov = get_provenance_from_events(r.id)
    assert prov == "conv:123"

    # delete the memory and ensure it's no longer retrieved
    store.delete_by_id(r.id)
    rows = retrieve_for_user(store, "userA")
    assert len(rows) == 0

    deletes = find_events(event_type="delete", memory_id=r.id)
    assert len(deletes) >= 1
    store.close()
