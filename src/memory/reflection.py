from typing import Optional


def consolidate_scattered_facts(store, user_id: str) -> Optional[object]:
    """Consolidate multiple low-level memories for `user_id` into a single summary memory.

    For the prototype: create a summary MemoryRecord whose content is the unique
    concatenation of existing contents, add it to the store, and delete the originals.
    Returns the new summary MemoryRecord or None if nothing consolidated.
    """
    rows = [r for r in store._records if r.user_id == user_id]
    if len(rows) < 2:
        return None
    unique_contents = sorted({r.content for r in rows})
    summary_text = "; ".join(unique_contents)
    try:
        from .schema import MemoryRecord

        summary = MemoryRecord(user_id=user_id, content=summary_text, importance=max((r.importance for r in rows), default=0.0), confidence=(sum((r.confidence for r in rows)) / len(rows)))
        # add summary and delete originals
        store.add(summary)
        for r in list(rows):
            store.delete_by_id(r.id)
        return summary
    except Exception:
        return None
