"""Append-only audit log for governance tests.

This module provides an in-memory audit log suitable for unit tests. Production
should replace with an append-only persistent store.
"""
from typing import List, Dict, Optional

_events: List[Dict] = []


def record(event_type: str, memory_id: Optional[str] = None, user_id: Optional[str] = None, details: Optional[Dict] = None):
    _events.append({
        "event_type": event_type,
        "memory_id": memory_id,
        "user_id": user_id,
        "details": details or {},
    })


def all_events() -> List[Dict]:
    return list(_events)


def find_events(event_type: Optional[str] = None, memory_id: Optional[str] = None):
    out = []
    for e in _events:
        if event_type and e.get("event_type") != event_type:
            continue
        if memory_id and e.get("memory_id") != memory_id:
            continue
        out.append(e)
    return out


def reset():
    _events.clear()
