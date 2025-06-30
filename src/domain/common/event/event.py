from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from didiator.interface.entities.event import Event as DidiatorBaseEvent

@dataclass(frozen=True)
class Event(DidiatorBaseEvent, ABC):
    event_id: UUID = field(default_factory=uuid4)
    event_timestamp: datetime = field(default_factory=datetime.now)
