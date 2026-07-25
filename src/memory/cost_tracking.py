"""Lightweight cost tracking for M6 economics prototype.

Tracks per-memory and per-operation costs so tests can compute $/useful-memory.
This is a prototype: replace with proper billing telemetry in production.
"""
from typing import Dict, List, Optional

_costs_by_memory: Dict[str, float] = {}
_events: List[Dict] = []
_deleted_ids: set = set()


def record_cost(memory_id: Optional[str], amount: float, category: str = "other"):
    _events.append({"memory_id": memory_id, "amount": float(amount), "category": category})
    if memory_id:
        _costs_by_memory[memory_id] = _costs_by_memory.get(memory_id, 0.0) + float(amount)


def total_cost() -> float:
    return sum(e["amount"] for e in _events)


def cost_for_memory(memory_id: str) -> float:
    return _costs_by_memory.get(memory_id, 0.0)


def mark_deleted(memory_id: str):
    _deleted_ids.add(memory_id)


def cost_per_useful_memory(records: List[object], importance_threshold: float = 0.5) -> Optional[float]:
    """Compute total cost for memories considered 'useful' divided by their count.

    A memory is useful if `record.importance >= importance_threshold` and it is not deleted.
    Returns None if there are zero useful memories.
    """
    useful_ids = [r.id for r in records if getattr(r, "importance", 0.0) >= importance_threshold and r.id not in _deleted_ids]
    if not useful_ids:
        return None
    total = sum(cost_for_memory(i) for i in useful_ids)
    return total / len(useful_ids)


def reset():
    _costs_by_memory.clear()
    _events.clear()
    _deleted_ids.clear()
