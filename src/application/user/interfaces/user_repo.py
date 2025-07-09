from abc import abstractmethod
from uuid import UUID
from typing_extensions import Protocol

from src.application.user.dto import UserDto
from src.domain.user.entity.user import User


class UserRepo(Protocol):
    @abstractmethod
    async def create_user(self, new_user: User) -> UserDto | None: ...

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> bool: ...
