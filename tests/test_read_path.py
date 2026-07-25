import os
import sys
from datetime import datetime, timedelta

# Ensure `src` is on the import path for tests (same pattern as other tests)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory.schema import MemoryRecord
from memory.store import MemoryStore
from memory.retriever import retrieve_for_user
from memory.ranking import rank_memories
from memory.context_composer import compose_context


def test_read_path_ranks_by_blend():
    store = MemoryStore()
    user = "user:1"

    now = datetime.utcnow()

    # High relevance memories (course-related)
    m1 = MemoryRecord(user_id=user, content="I design an online course about AI", importance=0.9)
    m1.created_at = now - timedelta(days=1)

    m2 = MemoryRecord(user_id=user, content="I teach course design and pedagogy", importance=0.8)
    m2.created_at = now - timedelta(hours=12)

    m3 = MemoryRecord(user_id=user, content="I build interactive course assignments", importance=0.85)
    m3.created_at = now - timedelta(days=2)

    # Low relevance memories
    m4 = MemoryRecord(user_id=user, content="I had coffee this morning", importance=0.1)
    m4.created_at = now - timedelta(days=10)

    m5 = MemoryRecord(user_id=user, content="I went jogging", importance=0.05)
    m5.created_at = now - timedelta(days=5)

    for m in (m1, m2, m3, m4, m5):
        store.add(m)

    all_mem = retrieve_for_user(store, user)
    ranked = rank_memories(all_mem, query="help me design a course", top_k=5)

    # Expect the three course-related memories to appear before the unrelated ones
    contents = [m.content for m in ranked]
    assert contents.index(m1.content) < contents.index(m4.content)
    assert contents.index(m2.content) < contents.index(m4.content)
    assert contents.index(m3.content) < contents.index(m4.content)

    # Compose a context block string and assert it's non-empty
    ctx = compose_context(ranked[:3])
    assert "course" in ctx.lower()
