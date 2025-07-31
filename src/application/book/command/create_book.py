from dataclasses import dataclass
from uuid import UUID

from src.application.book.dto import BookDto
from src.application.book.interfaces.book_repo import BookRepo
from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.common.interfaces.mapper import DomainMapper
from src.domain.book.entity import Book


@dataclass
class CreateBook(Command[BookDto]):
    title: str
    author: UUID


class CreateBookHandler(CommandHandler[CreateBook, BookDto]):
    def __init__(
        self,
        book_repo: BookRepo,
        uof: UnitOfWork,
        mapper: DomainMapper[Book, BookDto]
    ):
        self.book_repo = book_repo
        self.uof = uof
        self.mapper = mapper

    async def __call__(self, command: CreateBook) -> BookDto:
        new_book  = Book.create(
            author=command.author,
            title=command.title,
        )

        await self.book_repo.create_book(new_book)
        await self.uof.commit()

        return self.mapper.domain_to_dto(new_book)
