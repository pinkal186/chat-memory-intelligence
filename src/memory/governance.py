from typing import Optional
from .audit_log import find_events


def get_provenance_from_events(memory_id: str) -> Optional[str]:
    """Return the recorded `source` for a memory from the audit events if present."""
    writes = find_events(event_type="write", memory_id=memory_id)
    if not writes:
        return None
    # assume the first write's details contain the recorded source
    return writes[0].get("details", {}).get("source")
