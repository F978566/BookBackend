from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import delete

from src.application.common.interfaces.mapper import DomainMapper
from src.application.user.dto import UserDto
from src.application.user.interfaces.user_repo import UserRepo
from src.domain.user.entity.user import User
from src.infrastructure.db.models.user import UserModel


class UserRepoImpl(UserRepo):
    def __init__(self, session: AsyncSession, mapper: DomainMapper[User, UserDto]):
        self._session = session
        self._mapper = mapper

    async def create_user(self, new_user: User) -> UserDto | None:
        try:
            user = UserModel(
                username=new_user.username,
                password=new_user.password,
                email=new_user.email,
                user_role=tuple([x.value.name for x in new_user.user_role]),
                deleted=new_user.deleted,
            )
            self._session.add(user)

            return self._mapper.domain_to_dto(new_user)
        except:
            return None

    async def delete_user(self, user_id: UUID) -> bool:
        try:
            await self._session.execute(delete(UserModel).where(UserModel.id == user_id))
            return True
        except:
            return False
