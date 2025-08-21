from dataclasses import dataclass
from uuid import UUID

from src.application.book.dto.book import BookDto
from src.application.book.interfaces.book_repo import BookRepo
from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.mapper import DomainMapper
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.dto.user import UserDto
from src.application.user.interfaces.user_repo import UserRepo
from src.domain.book.entity.book import Book
from src.domain.user.entity.user import User


@dataclass
class AddBookRedactor(Command[None]):
    book_id: UUID
    redactor_id: UUID
    new_redactor_id: UUID


class AddBookRedactorHandler(CommandHandler[AddBookRedactor, None]):
    def __init__(
        self,
        book_repo: BookRepo,
        user_repo: UserRepo,
        book_mapper: DomainMapper[Book, BookDto],
        user_mapper: DomainMapper[User, UserDto],
        uof: UnitOfWork,
    ):
        self.book_repo = book_repo
        self.user_repo = user_repo
        self.book_mapper = book_mapper
        self.user_mapper = user_mapper
        self.uof = uof

    async def __call__(self, request: AddBookRedactor) -> None:
        user = await self.user_repo.get_user_by_id(request.new_redactor_id)
        book = await self.book_repo.get_book_by_id(request.book_id)

        domain_book = self.book_mapper.dto_to_domain(book)
        domain_book.add_redactor(request.redactor_id, self.user_mapper.dto_to_domain(user))

        await self.book_repo.add_author(request.book_id, request.new_redactor_id)
        await self.uof.commit()
