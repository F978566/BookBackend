from abc import abstractmethod
from uuid import UUID
from typing import Protocol

from src.application.user.dto import UserDto
from src.domain.user.entity.user import User
from src.domain.user.value_object.user_role_enum import UserRoleEnum


class UserRepo(Protocol):
    @abstractmethod
    async def create_user(self, new_user: User) -> None: ...

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> bool: ...

    @abstractmethod
    async def add_user_role(self, user_id: UUID, user_role: UserRoleEnum) -> None: ...

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> UserDto: ...
