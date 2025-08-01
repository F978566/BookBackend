from abc import ABC
from dataclasses import dataclass, field

from ..event.event import Event
from .entity import Entity


@dataclass
class AgregateRoot(Entity, ABC):
    _events: list[Event] = field(default_factory=list)

    def record_event(self, event: Event) -> None:
        self._events.append(event)

    def get_events(self) -> list[Event]:
        return self._events

    def clear_events(self) -> None:
        self._events.clear()

    def pull_events(self) -> list[Event]:
        return [self._events.pop() for _ in range(len(self._events))]
