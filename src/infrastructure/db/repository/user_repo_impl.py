from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import delete

from application.common.interfaces.mapper import Mapper
from application.user.dto import UserDto
from application.user.interfaces.user_repo import UserRepo
from domain.user.entity.user import User
from infrastructure.db.models.user import UserModel


class UserRepoImpl(UserRepo):
    def __init__(self, session: AsyncSession, mapper: Mapper[User, UserDto]):
        self._session = session
        self._mapper = mapper

    async def create_user(self, new_user: User) -> UserDto | None:
        try:
            user = UserModel(
                username=new_user.username,
                password=new_user.password,
                email=new_user.email,
                user_role=new_user.user_role.value,
                deleted=new_user.deleted,
            )
            self._session.add(user)

            # await self._session.commit()
            # await self._session.refresh(user)

            return self._mapper.domain_to_dto(new_user)
        except:
            return None

    async def delete_user(self, user_id: UUID) -> bool:
        try:
            await self._session.execute(delete(UserModel).where(UserModel.id == user_id))
            return True
        except:
            return False
