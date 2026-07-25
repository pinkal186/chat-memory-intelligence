import os
import sys

# Ensure `src` is on the import path for tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory import extract_memories, evaluate_candidate, MemoryStore


def run_pipeline(turn_text: str, user_id: str = "user:1"):
    store = MemoryStore()
    candidates = extract_memories(turn_text, user_id=user_id)
    for c in candidates:
        if evaluate_candidate(c):
            store.add(c)
    return store


def test_write_path_writes_expected_records():
    text = "I use PostgreSQL and I'm building SecondBrainLabs"
    store = run_pipeline(text, user_id="u1")
    rows = store.query_by_user("u1")
    assert len(rows) == 2, f"expected 2 records, got {len(rows)}"
    for r in rows:
        assert r.importance > 0
        assert r.confidence > 0
        assert r.source == "turn"


def test_write_path_drops_low_utility():
    text = "I had coffee today"
    store = run_pipeline(text, user_id="u2")
    rows = store.query_by_user("u2")
    assert len(rows) == 0, f"expected 0 records, got {len(rows)}"
