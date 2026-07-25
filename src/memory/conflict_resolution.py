def resolve_conflict_on_write(store, new_record) -> bool:
    """Prototype conflict resolution: if an existing record has identical user_id and type,
    prefer the newer record if content differs; otherwise keep both.

    Returns True if a resolution was applied (older record removed), False otherwise.
    """
    for r in list(store._records):
        if r.user_id == new_record.user_id and r.type == new_record.type and r.content != new_record.content:
            # simple rule: delete the older record and keep the new one
            store.delete_by_id(r.id)
            return True
    return False
