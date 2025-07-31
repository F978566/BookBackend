# from didiator.interface import Mediator
from dishka import Provider, Scope, provide # type: ignore
import redis
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncIterator
from passlib.context import CryptContext
# from dishka import make_async_container
# from didiator import Mediator

from src.application.book.command.add_book_page import AddBookPageHandler
from src.application.book.interfaces.book_repo import BookRepo
from src.application.common.interfaces.db_model_mapper import DbModelMapper
from src.infrastructure.db.models.book import BookModel
from src.infrastructure.db.repository.book_repo_impl import BookRepoImpl
from src.infrastructure.mapper.book_db_model_mapper import BookDbModelMapper
from src.infrastructure.mapper.book_mapper import BookMapper
from src.infrastructure.mapper.page_mapper import PageMapper
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces.user_repo import UserRepo
from src.infrastructure.db.repository.user_repo_impl import UserRepoImpl
from src.application.common.interfaces.mapper import DomainMapper
from src.domain.user.entity.user import User
from src.domain.book.entity import Book, Page
from src.application.user.dto import UserDto
from src.application.book.dto import BookDto, PageDto
from src.application.user.utils import PasswordEncryptor
from src.application.user.command.create_user import CreateUserHandler
from src.infrastructure.mapper.user_mapper import UserMapper
from src.infrastructure.db.base import async_session_factory
from src.application.book.command.create_book import CreateBookHandler
# from src.di.mediator import build_mediator
from src.infrastructure.db.uof import SQLAlchemyUoW


class AppContainer(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_db(self) -> AsyncIterator[AsyncSession]:
        async with async_session_factory() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def provide_user_repository(self, session: AsyncSession, mapper: DomainMapper[User, UserDto]) -> UserRepo:
        return UserRepoImpl(
            session=session,
            mapper=mapper,
        )

    @provide(scope=Scope.REQUEST)
    def provide_create_user_command_handler(
        self,
        user_repo: UserRepo,
        uof: UnitOfWork,
        mapper: DomainMapper[User, UserDto],
        password_encryptor: PasswordEncryptor,
        # mediator: Mediator,
    ) -> CreateUserHandler:
        return CreateUserHandler(user_repo, uof, mapper, password_encryptor)

    @provide(scope=Scope.REQUEST)
    def provide_user_mapper(self) -> DomainMapper[User, UserDto]:
        return UserMapper()

    @provide(scope=Scope.REQUEST)
    def provide_book_mapper(self) -> DomainMapper[Book, BookDto]:
        return BookMapper()

    @provide(scope=Scope.REQUEST)
    def provide_page_mapper(self) -> DomainMapper[Page, PageDto]:
        return PageMapper()

    @provide(scope=Scope.REQUEST)
    def provide_unit_of_work(self, session: AsyncSession) -> UnitOfWork:
        return SQLAlchemyUoW(session)

    @provide(scope=Scope.APP)
    def get_crypt_context(self) -> CryptContext:
        return CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    @provide(scope=Scope.REQUEST)
    def provide_password_encryptor(self, crypt_context: CryptContext) -> PasswordEncryptor:
        return PasswordEncryptor(crypt_context)

    @provide(scope=Scope.REQUEST)
    def provide_book_repo(
        self,
        session: AsyncSession,
        book_mapper: DbModelMapper[BookDto, BookModel],
        redis: redis.Redis,
    ) -> BookRepo:
        return BookRepoImpl(session, book_mapper, redis)
    
    @provide(scope=Scope.REQUEST)
    def provide_db_book_model_wrapper(self) -> DbModelMapper[BookDto, BookModel]:
        return BookDbModelMapper()

    @provide(scope=Scope.REQUEST)
    def provide_create_book_command_handler(
        self,
        book_repo: BookRepo,
        uof: UnitOfWork,
        mapper: DomainMapper[Book, BookDto],
        # mediator: Mediator,
    ) -> CreateBookHandler:
        return CreateBookHandler(book_repo, uof, mapper)

    @provide(scope=Scope.REQUEST)
    def provide_add_book_page_command_handler(
        self,
        book_repo: BookRepo,
        uof: UnitOfWork,
        mapper: DomainMapper[Page, PageDto],
        # mediator: Mediator,
    ) -> AddBookPageHandler:
        return AddBookPageHandler(book_repo, uof, mapper)
    
    @provide(scope=Scope.APP)
    def provide_redis(self) -> redis.Redis:
        return redis.Redis(host='localhost', port=6379, db=0)

    # @provide(scope=Scope.APP)
    # def provide_mediator(self) -> Mediator:
    #     return build_mediator(make_async_container(self))
