from dataclasses import dataclass, field
from uuid import UUID
from domain.common.event.event import Event


@dataclass(frozen=True)
class UserDeleted(Event):
    user_id: UUID = field(kw_only=True)