import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory.metrics import reset, get_counter, get_histogram
from memory.store import MemoryStore
from memory.schema import MemoryRecord
from memory.retriever import retrieve_for_user


def test_observability_emits_metrics_on_read_write():
    reset()
    store = MemoryStore()

    m = MemoryRecord(user_id="u1", content="observable fact")
    store.add(m)

    # write counter incremented
    assert get_counter("memory_write_count") >= 1

    rows = retrieve_for_user(store, "u1")
    assert len(rows) == 1

    # retrieval counter and latency histograms emitted
    assert get_counter("memory_retrieval_count") >= 1
    assert isinstance(get_histogram("memory_write_latency_ms"), list)
    assert isinstance(get_histogram("memory_retrieval_latency_ms"), list)
    assert len(get_histogram("memory_write_latency_ms")) >= 1
    assert len(get_histogram("memory_retrieval_latency_ms")) >= 1
