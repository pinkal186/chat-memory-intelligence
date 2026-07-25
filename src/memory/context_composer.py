from typing import List
from .schema import MemoryRecord


def compose_context(memories: List[MemoryRecord]) -> str:
    """Assemble a human-readable context block from ranked memories."""
    if not memories:
        return ""
    lines = []
    for i, m in enumerate(memories, start=1):
        lines.append(f"{i}. {m.content} (importance={m.importance:.2f})")
    return "\n".join(lines)
