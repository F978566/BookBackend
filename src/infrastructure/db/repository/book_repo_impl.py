from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import update, select

from src.application.common.interfaces.mapper import Mapper
from src.infrastructure.db.models.book import BookModel, PageModel
from src.infrastructure.db.models.user import UserModel
from src.application.book.interfaces.book_repo import BookRepo
from src.domain.book.entity import Book
from src.application.book.dto.book import BookDto
from src.domain.book.entity import Page
from src.application.book.dto.page import PageDto
from src.domain.book.value_objects.book_status_enum import BookStatusEnum


class BookRepoImpl(BookRepo):
    def __init__(
        self,
        session: AsyncSession,
        book_mapper: Mapper[Book, BookDto],
        page_mapper: Mapper[Page, PageDto],
    ):
        self._session = session
        self._book_mapper = book_mapper
        self._page_mapper = page_mapper

    async def create_book(self, book: Book) -> BookDto:
        new_book_model = BookModel(
            title=book.title,
            size=book.size,
        )
        self._session.add(new_book_model)

        return self._book_mapper.domain_to_dto(book)

    async def add_book_page(
        self,
        book_id: UUID,
        page: Page,
    ) -> PageDto:
        print(book_id, page)
        new_page_model = PageModel(
            book_id=book_id,
            text=page.text,
            number=page.number,
        )

        await self._session.execute(
            update(BookModel)
            .where(BookModel.id==book_id)
            .values(size=BookModel.size + 1)
        )
        self._session.add(new_page_model)

        return self._page_mapper.domain_to_dto(page)

    async def set_status(self, status: BookStatusEnum) -> bool:
        try:
            await self._session.execute(
                update(BookModel.status).values(status.value)
            )

            return True
        except:
            return False

    async def add_redactor(self, book_id: UUID, redactor_id: UUID) -> bool:
        book_model = (await self._session.execute(select(BookModel).where(BookModel.id==book_id))).scalar()

        if book_model is None:
            return False

        redactor_model = (await self._session.execute(select(UserModel).where(UserModel.id==redactor_id))).scalar()

        if redactor_model is None:
            return False

        book_model.redactors.append(redactor_model)

        return True

    async def add_author(self, book_id: UUID, author_id: UUID) -> bool:
        book_model = (await self._session.execute(select(BookModel).where(BookModel.id==book_id))).scalar()

        if book_model is None:
            return False

        author_model = (await self._session.execute(select(UserModel).where(UserModel.id==author_id))).scalar()

        if author_model is None:
            return False

        book_model.redactors.append(author_model)

        return True
