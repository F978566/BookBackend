from dataclasses import dataclass
from didiator import EventMediator

from application.common.interfaces.uow import UnitOfWork
from application.user.dto.user import UserDto
from application.user.interfaces.user_repo import UserRepo
from application.common.interfaces.mapper import Mapper
from domain.user.entity.user import User
from domain.user.value_object.user_role_enum import UserRoleEnum
from domain.user.value_object.user_role import UserRole
from ...common.command import Command, CommandHandler

@dataclass
class CreateUser(Command[UserDto]):
    username: str
    password: str
    email: str
    user_role: UserRoleEnum


class CreateUserHandler(CommandHandler[CreateUser, UserDto]):
    def __init__(
        self,
        user_repo: UserRepo,
        uof: UnitOfWork,
        mapper: Mapper[User, UserDto],
        mediator: EventMediator,
    ):
        self.user_repo = user_repo
        self.uof = uof
        self.mapper = mapper
        self.mediator = mediator

    async def handle(self, command: CreateUser) -> UserDto:
        user = User.create(
            username=command.username,
            password=command.password,
            email=command.email,
            user_role=UserRole(command.user_role),
        )
        await self.user_repo.create_user(user)
        await self.uof.commit()
        await self.mediator.publish(user.pull_events())
        return self.mapper.domain_to_dto(user)
