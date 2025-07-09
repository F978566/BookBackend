from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.domain.common.event.event import Event
from src.domain.user.value_object.user_role_enum import UserRoleEnum


@dataclass(frozen=True)
class UserCreated(Event):
    username: str = field(default="")
    password: str = field(default="")
    email: str = field(default="")
    user_role: UserRoleEnum = field(default=UserRoleEnum.READER)
    id: UUID = field(default_factory=uuid4)
