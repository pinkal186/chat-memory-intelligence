from typing import List
from .schema import MemoryRecord
from . import metrics, tracing, cost_tracking


def retrieve_for_user(store, user_id: str) -> List[MemoryRecord]:
    """Return all memories for a user from the provided store.

    Emits observability signals: `memory_retrieval_count`, `memory_retrieval_latency_ms`,
    and `memory_retrieval_failures` on exceptions.
    """
    try:
        with tracing.timer("memory_retrieval_latency_ms"):
            rows = store.query_by_user(user_id)
        metrics.incr("memory_retrieval_count")
        try:
            # Prototype: record retrieval-level cost event
            cost_tracking.record_cost(None, 0.02, "retrieval")
        except Exception:
            pass
        return rows
    except Exception:
        # On store failure, degrade gracefully by returning no memories.
        metrics.incr("memory_retrieval_failures")
        return []
