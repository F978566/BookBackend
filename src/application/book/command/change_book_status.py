from dataclasses import dataclass
from uuid import UUID

from src.application.book.dto.book import BookDto
from src.application.book.interfaces.book_repo import BookRepo
from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.mapper import DomainMapper
from src.application.common.interfaces.uow import UnitOfWork
from src.domain.book.entity.book import Book
from src.domain.book.value_objects.book_status_enum import BookStatusEnum


@dataclass
class ChangeBookStatus(Command[None]):
    book_id: UUID
    user_id: UUID
    status: BookStatusEnum


class ChangeBookStatusHandler(CommandHandler[ChangeBookStatus, None]):
    def __init__(
        self,
        book_repo: BookRepo,
        mapper: DomainMapper[Book, BookDto],
        uof: UnitOfWork,
    ):
        self.book_repo = book_repo
        self.mapper = mapper
        self.uof = uof

    async def __call__(self, request: ChangeBookStatus) -> None:
        book = await self.book_repo.get_book_by_id(request.book_id)

        domain_book = self.mapper.dto_to_domain(book)

        domain_book.change_book_status(
            request.user_id,
            request.status,
        )

        await self.book_repo.set_status(book_id=request.book_id, status=request.status)
        await self.uof.commit()
