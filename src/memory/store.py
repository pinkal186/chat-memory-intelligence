from typing import List
from .schema import MemoryRecord
from . import metrics, tracing, audit_log, cost_tracking


class MemoryStore:
    """In-memory memory store used for M1 unit tests."""

    def __init__(self):
        self._records: List[MemoryRecord] = []

    def add(self, record: MemoryRecord):
        # Instrument write path: count + latency
        metrics.incr("memory_write_count")
        with tracing.timer("memory_write_latency_ms"):
            self._records.append(record)
        # Audit record the write
        try:
            audit_log.record("write", memory_id=record.id, user_id=record.user_id, details={"source": record.source})
        except Exception:
            pass
        try:
            # Record an example embedding cost for this write (prototype value)
            cost_tracking.record_cost(record.id, 0.50, "embedding")
            cost_tracking.record_cost(record.id, 0.01, "storage")
        except Exception:
            pass

    def query_by_user(self, user_id: str) -> List[MemoryRecord]:
        # Instrument read path: count + latency
        with tracing.timer("memory_retrieval_latency_ms"):
            out = [r for r in self._records if r.user_id == user_id]
        metrics.incr("memory_retrieval_count")
        try:
            audit_log.record("read", user_id=user_id, details={"count": len(out)})
        except Exception:
            pass
        try:
            # Record a prototype retrieval cost per call
            cost_tracking.record_cost(None, 0.02, "retrieval")
        except Exception:
            pass
        return out

    def clear(self):
        self._records.clear()

    def delete_by_id(self, memory_id: str):
        # Remove in-memory record and append audit event
        before = len(self._records)
        self._records = [r for r in self._records if r.id != memory_id]
        if len(self._records) < before:
            try:
                audit_log.record("delete", memory_id=memory_id)
            except Exception:
                pass
            try:
                cost_tracking.mark_deleted(memory_id)
            except Exception:
                pass
