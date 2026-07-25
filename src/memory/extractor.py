from .schema import MemoryRecord
from typing import List

def extract_memories(turn_text: str, user_id: str = "user:1") -> List[MemoryRecord]:
    """Very small heuristic extractor for M1.

    Splits on ' and ' and looks for first-person assertions as memories.
    """
    text = turn_text.strip()
    lower = text.lower()
    candidates: List[MemoryRecord] = []

    # Simple heuristics for extraction
    triggers = ["i use", "i'm", "i am", "i have", "i run", "i work", "i build", "i'm building"]

    if any(t in lower for t in triggers):
        # split into clauses loosely
        parts = [p.strip() for p in text.replace("I'm", "I am").split(" and ") if p.strip()]
        for part in parts:
            if len(part) < 6:
                continue
            rec = MemoryRecord(user_id=user_id, content=part, source="turn")
            candidates.append(rec)

    return candidates
