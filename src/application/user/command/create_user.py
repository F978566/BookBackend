from dataclasses import dataclass
# from didiator import EventMediator
# from didiator import Mediator

from src.application.user.utils.password_encryptor import PasswordEncryptor
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.dto.user import UserDto
from src.application.user.interfaces.user_repo import UserRepo
from src.application.common.interfaces.mapper import Mapper
from src.domain.user.entity.user import User
from src.domain.user.value_object.user_role_enum import UserRoleEnum
from src.domain.user.value_object.user_role import UserRole
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
        password_encryptor: PasswordEncryptor,
        # mediator: Mediator,
    ):
        self.user_repo = user_repo
        self.uof = uof
        self.mapper = mapper
        self.password_encryptor = password_encryptor
        # self.mediator = mediator

    async def __call__(self, command: CreateUser) -> UserDto:
        user = User.create(
            username=command.username,
            password=self.password_encryptor.encrypt_password(command.password),
            email=command.email,
            user_role=UserRole(command.user_role),
        )
        await self.user_repo.create_user(user)
        await self.uof.commit()
        # await self.mediator.publish(user.pull_events())
        return self.mapper.domain_to_dto(user)
