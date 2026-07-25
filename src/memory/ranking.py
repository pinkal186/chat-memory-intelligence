from typing import List
from datetime import datetime
from .schema import MemoryRecord
import math


def _semantic_score(content: str, query: str) -> float:
    # simple bag-of-words overlap
    q_words = [w for w in query.lower().split() if w]
    if not q_words:
        return 0.0
    c_words = content.lower().split()
    matches = sum(1 for w in q_words if w in c_words)
    return matches / len(q_words)


def _recency_score(created_at: datetime, now: datetime) -> float:
    # newer -> higher. Use 1 / (1 + age_days)
    age_days = max(0.0, (now - created_at).total_seconds() / 86400.0)
    return 1.0 / (1.0 + age_days)


def _frequency_scores(memories: List[MemoryRecord]) -> dict:
    counts = {}
    for m in memories:
        counts[m.content] = counts.get(m.content, 0) + 1
    maxc = max(counts.values()) if counts else 1
    return {content: cnt / maxc for content, cnt in counts.items()}


def rank_memories(memories: List[MemoryRecord], query: str, top_k: int = 5) -> List[MemoryRecord]:
    now = datetime.utcnow()
    freq_map = _frequency_scores(memories)

    scored = []
    for m in memories:
        sem = _semantic_score(m.content, query)
        rec = _recency_score(m.created_at, now)
        freq = freq_map.get(m.content, 0.0)
        importance = float(getattr(m, "importance", 0.0))

        score = 0.4 * sem + 0.2 * rec + 0.2 * freq + 0.2 * importance
        scored.append((score, m))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored[:top_k]]
