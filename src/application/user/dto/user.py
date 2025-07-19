from dataclasses import dataclass, field
from uuid import UUID

from src.application.dto import DTO
from src.domain.user.value_object.user_role_enum import UserRoleEnum


@dataclass(frozen=True)
class UserDto(DTO):
    id: UUID
    username: str
    password: str
    email: str
    user_role: list[UserRoleEnum]
    deleted: bool = field(default=False, kw_only=True)
