import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from memory.cost_tracking import reset, total_cost, cost_per_useful_memory, cost_for_memory
from memory.store import MemoryStore
from memory.schema import MemoryRecord


def test_costs_and_useful_memory():
    reset()
    store = MemoryStore()

    # high-importance memories
    m1 = MemoryRecord(user_id="u", content="A", importance=0.9)
    m2 = MemoryRecord(user_id="u", content="B", importance=0.8)

    # low-importance memory (should be excluded)
    m3 = MemoryRecord(user_id="u", content="C", importance=0.1)

    store.add(m1)
    store.add(m2)
    store.add(m3)

    # total cost should be > 0
    assert total_cost() > 0

    # cost per useful memory (importance >= 0.5) should compute using two memories
    c = cost_per_useful_memory([m1, m2, m3], importance_threshold=0.5)
    assert c is not None
    # individual memory cost recorded
    assert cost_for_memory(m1.id) >= 0.5

    # delete one useful memory and ensure denominator drops
    store.delete_by_id(m2.id)
    c2 = cost_per_useful_memory([m1, m2, m3], importance_threshold=0.5)
    assert c2 is not None
    # since only one useful memory remains, cost_per_useful_memory should equal cost_for_memory(m1.id)
    assert abs(c2 - cost_for_memory(m1.id)) < 1e-6
