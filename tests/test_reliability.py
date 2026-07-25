import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory.retriever import retrieve_for_user


class FlakyStore:
    def query_by_user(self, user_id: str):
        raise RuntimeError("simulated store outage")


def test_retriever_degrades_on_store_failure():
    store = FlakyStore()
    # Should not raise, and should return empty list on failure
    rows = retrieve_for_user(store, "any")
    assert rows == []
