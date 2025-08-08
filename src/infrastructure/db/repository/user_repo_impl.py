from uuid import UUID
from sqlalchemy.dialects.postgresql.base import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import delete
from sqlalchemy.orm import attributes

from src.application.common.interfaces.db_model_mapper import DbModelMapper
from src.application.user.dto import UserDto
from src.application.user.interfaces.user_repo import UserRepo
from src.domain.user.entity.user import User
from src.domain.user.value_object.user_role_enum import UserRoleEnum
from src.infrastructure.db.models.user import UserModel


class UserRepoImpl(UserRepo):
    def __init__(self, session: AsyncSession, mapper: DbModelMapper[UserDto, UserModel]):
        self._session = session
        self._mapper = mapper

    async def create_user(self, new_user: User) -> None:
        try:
            user = UserModel(
                username=new_user.username,
                password=new_user.password,
                email=new_user.email,
                user_role=tuple([x.value.name.upper() for x in new_user.user_role]),
                deleted=new_user.deleted,
            )
            self._session.add(user)
        except:
            return None

    async def delete_user(self, user_id: UUID) -> bool:
        try:
            await self._session.execute(delete(UserModel).where(UserModel.id == user_id))
            return True
        except:
            return False

    async def add_user_role(self, user_id: UUID, user_role: UserRoleEnum) -> None:
        try:
            user = (await self._session.execute(
                select(UserModel)
                .where(UserModel.id == user_id)
            )).scalar()

            user.user_role.append(user_role)
            attributes.flag_modified(user, "user_role")
        except:
            return None

    async def get_user_by_id(self, user_id: UUID) -> UserDto:
        user = (await self._session.execute(
            select(UserModel)
            .where(UserModel.id == user_id)
        )).scalar_one_or_none()

        if user is None:
            raise ValueError()

        return self._mapper.db_model_to_dto(user)
