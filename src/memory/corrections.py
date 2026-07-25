from typing import Optional


def apply_correction(store, memory_id: str, new_content: Optional[str] = None, new_confidence: Optional[float] = None) -> bool:
    """Apply a user correction to an existing memory identified by `memory_id`.

    Returns True if an existing memory was updated, False otherwise.
    """
    for r in store._records:
        if r.id == memory_id:
            if new_content is not None:
                r.content = new_content
            if new_confidence is not None:
                r.confidence = float(new_confidence)
            try:
                from . import audit_log

                audit_log.record("correction", memory_id=r.id, user_id=r.user_id, details={"content": r.content, "confidence": r.confidence})
            except Exception:
                pass
            return True
    return False
