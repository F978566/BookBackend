from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
# from didiator import Mediator

from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces.user_repo import UserRepo
from src.infrastructure.db.repository.user_repo_impl import UserRepoImpl
from src.application.common.interfaces.mapper import Mapper
from src.domain.user.entity.user import User
from src.application.user.dto import UserDto
from src.application.user.command.create_user import CreateUserHandler
from src.infrastructure.mapper.user_mapper import UserMapper
from src.infrastructure.db.base import async_session_factory
from src.infrastructure.db.uof import SQLAlchemyUoW


class AppContainer(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_db(self) -> AsyncIterator[AsyncSession]:
        async with async_session_factory() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def provide_user_repository(self, session: AsyncSession, mapper: Mapper[User, UserDto]) -> UserRepo:
        return UserRepoImpl(
            session=session,
            mapper=mapper,
        )

    @provide(scope=Scope.REQUEST)
    def provide_create_user_command_handler(
        self,
        user_repo: UserRepo,
        uof: UnitOfWork,
        mapper: Mapper[User, UserDto],
        # mediator: Mediator,
    ) -> CreateUserHandler:
        return CreateUserHandler(user_repo, uof, mapper)

    @provide(scope=Scope.REQUEST)
    def provide_user_mapper(self) -> Mapper[User, UserDto]:
        return UserMapper()

    @provide(scope=Scope.REQUEST)
    def provide_unit_of_work(self, session: AsyncSession) -> UnitOfWork:
        return SQLAlchemyUoW(session)

    # @provide(scope=Scope.REQUEST)
    # def get_event_mediator(self, dishka_container) -> EventMediator:
    #     di_builder = DiBuilderImpl(
    #         di_container=dishka_container,
    #         di_executor=None,
    #         di_scopes=["request"]
    #     )

    #     middlewares = [
    #         DiMiddleware(di_builder, scopes=DiScopes("request"))
    #     ]

    #     event_observer = EventObserverImpl(middlewares=middlewares)
    #     event_mediator = EventMediatorImpl(event_observer=event_observer)

    #     return EventMediator(builder=di_builder)
