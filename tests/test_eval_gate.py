import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory.eval_harness import run_golden_set
from memory.store import MemoryStore
from memory.schema import MemoryRecord


def test_eval_gate_against_golden_set(tmp_path):
    # Prepare a store with deterministic memory ids referenced by the golden set
    store = MemoryStore()
    store.add(MemoryRecord(id="m-1", user_id="user-a", content="I like VSCode", importance=0.9))
    store.add(MemoryRecord(id="m-2", user_id="user-a", content="Also configure with settings.json", importance=0.7))
    store.add(MemoryRecord(id="m-3", user_id="user-b", content="Prefer PyCharm for heavy refactors", importance=0.8))

    path = os.path.join(os.path.dirname(__file__), "data", "golden_set.jsonl")
    res = run_golden_set(path, store, lambda s, u: __import__("memory.retriever", fromlist=["retrieve_for_user"]).retrieve_for_user(s, u))
    # Basic sanity: at least one case, precision and recall are > 0
    assert res["cases"] >= 1
    assert res["precision"] >= 0.5
    assert res["recall"] >= 0.5
