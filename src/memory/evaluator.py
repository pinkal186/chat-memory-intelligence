from .schema import MemoryRecord

def evaluate_candidate(record: MemoryRecord) -> bool:
    """Assign importance/confidence and return True if the candidate should be stored.

    Heuristic: longer content and presence of domain keywords => keep.
    """
    text = record.content.lower()
    keywords = ["use", "postgres", "postgresql", "build", "building", "work", "company", "deploy", "project", "sells"]

    score = 0.0
    if len(text) > 10:
        score += 0.6
    if any(k in text for k in keywords):
        score += 0.4

    # normalize to 0..1
    importance = min(1.0, score)
    confidence = 0.9 if importance > 0.5 else 0.2

    record.importance = importance
    record.confidence = confidence

    return importance > 0.5
