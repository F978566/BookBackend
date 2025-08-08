from dataclasses import dataclass
from uuid import UUID

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces import user_repo
from src.application.user.interfaces.user_repo import UserRepo
from src.domain.user.value_object.user_role_enum import UserRoleEnum

@dataclass(frozen=True)
class AddUserRole(Command[None]):
    user_id: UUID
    role: UserRoleEnum

class AddUserRoleHandler(CommandHandler[AddUserRole, None]):
    def __init__(self, user_repo: UserRepo, uof: UnitOfWork):
        self.user_repo = user_repo
        self.uof = uof

    async def __call__(self, request: AddUserRole) -> None:
        await self.user_repo.add_user_role(request.user_id, request.role)
        await self.uof.commit()
