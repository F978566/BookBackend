from dataclasses import dataclass, field

from src.domain.common.event.event import Event

@dataclass(frozen=True)
class PageAdded(Event):
    page_numbrer: int = field(default_factory=int)
    text: str = field(default_factory=str)
