from dataclasses import dataclass
from uuid import UUID, uuid4

from domain.common.event.event import Event
from domain.user.value_object.user_role_enum import UserRoleEnum


@dataclass(frozen=True)
class UserCreated(Event):
    username: str = ""
    password: str = ""
    email: str = ""
    user_role: UserRoleEnum = UserRoleEnum.READER
    id: UUID = uuid4()