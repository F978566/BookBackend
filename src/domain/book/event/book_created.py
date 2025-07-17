from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.domain.common.event.event import Event

@dataclass(frozen=True)
class BookCreated(Event):
    title: str = field(default_factory=str)
    author: UUID = field(default_factory=uuid4)
