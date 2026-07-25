from typing import List


def forget_by_content(store, user_id: str, substring: str) -> int:
    """Delete memories for `user_id` whose content contains `substring`.

    Returns the number of deleted memories.
    """
    to_delete: List[str] = [r.id for r in store._records if r.user_id == user_id and substring in r.content]
    for mid in to_delete:
        store.delete_by_id(mid)
    return len(to_delete)
