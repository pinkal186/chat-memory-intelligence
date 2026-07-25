from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class MemoryRecord:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = "default"
    type: str = "fact"
    content: str = ""
    importance: float = 0.0
    confidence: float = 0.0
    source: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
