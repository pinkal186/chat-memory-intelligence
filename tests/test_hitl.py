import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory.store import MemoryStore
from memory.schema import MemoryRecord

from memory.corrections import apply_correction
from memory.forget import forget_by_content


def test_hitl_correction_and_forget():
    store = MemoryStore()

    m = MemoryRecord(user_id="u1", content="works in EdTech", confidence=0.5)
    store.add(m)

    # apply a correction to the existing memory
    updated = apply_correction(store, m.id, new_content="runs a B2B SaaS", new_confidence=0.9)
    assert updated is True
    rows = store.query_by_user("u1")
    assert len(rows) == 1
    assert rows[0].content == "runs a B2B SaaS"
    assert rows[0].confidence == 0.9

    # add another memory and then forget it by content substring
    m2 = MemoryRecord(user_id="u1", content="I mentioned Kashmir recently")
    store.add(m2)
    deleted = forget_by_content(store, "u1", "Kashmir")
    assert deleted == 1
    rows = store.query_by_user("u1")
    assert all("Kashmir" not in r.content for r in rows)
