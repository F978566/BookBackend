from dataclasses import dataclass
from uuid import UUID

from src.application.common.interfaces.mapper import Mapper
from src.domain.book.entity import Page
from src.application.book.dto import PageDto
from src.application.book.interfaces.book_repo import BookRepo
from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork


@dataclass
class AddBookPage(Command[PageDto]):
    book_id: UUID
    number: int
    text: str



class AddBookPageHandler(CommandHandler[AddBookPage, PageDto]):
    def __init__(
        self,
        book_repo: BookRepo,
        uof: UnitOfWork,
        mapper: Mapper[Page, PageDto]
    ):
        self.book_repo = book_repo
        self.uof = uof
        self.mapper = mapper

    async def __call__(self, command: AddBookPage) -> PageDto:
        new_page = Page(
            number=command.number,
            text=command.text,
        )
        page = await self.book_repo.add_book_page(
            command.book_id,
            new_page,
        )

        await self.uof.commit()

        return page
