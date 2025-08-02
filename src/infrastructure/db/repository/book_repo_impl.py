import json
from typing import List
from uuid import UUID
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import update, select
from sqlalchemy.orm import selectinload
import dataclasses

from src.application.common.interfaces.db_model_mapper import DbModelMapper
from src.infrastructure.db.models.book import BookModel, PageModel
from src.infrastructure.db.models.user import UserModel
from src.application.book.interfaces.book_repo import BookRepo
from src.domain.book.entity import Book
from src.application.book.dto.book import BookDto
from src.domain.book.entity import Page
from src.domain.book.value_objects.book_status_enum import BookStatusEnum


class BookRepoImpl(BookRepo):
    def __init__(
        self,
        session: AsyncSession,
        book_mapper: DbModelMapper[BookDto, BookModel],
        redis: Redis,
    ):
        self._session = session
        self._book_mapper = book_mapper
        self.redis = redis

    async def create_book(
        self,
        book: Book,
        author_id: UUID,
    ) -> None:
        new_book_model = BookModel(
            title=book.title,
            size=book.size,
        )
        author = (await self._session.execute(
            select(UserModel)
            .where(UserModel.id == author_id)
            .options(selectinload(UserModel.author_books)) # type: ignore
        )).scalar()
        self._session.add(new_book_model)
        author.author_books.append(new_book_model) # type: ignore

    async def add_book_page(
        self,
        book_id: UUID,
        page: Page,
    ) -> None:
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

    async def get_all_books_by_author(self, author_id: UUID) -> List[BookDto]:
        cached_books = await self.redis.get(f"author_{author_id}")
        
        if cached_books:
            books_data = json.loads(cached_books)
            return [BookDto(**book_data) for book_data in books_data]
        
        books = (await self._session.execute(
            select(BookModel)
            .where(BookModel.authors.any(UserModel.id == author_id))
            .options(
                selectinload(BookModel.authors), # type: ignore
                selectinload(BookModel.redactors), # type: ignore
                selectinload(BookModel.pages), # type: ignore
            )
        )).scalars()

        res = [
            self._book_mapper.db_model_to_dto(book)
            for book in books
        ]

        books_json = json.dumps([dataclasses.asdict(book) for book in res], default=str)
        
        
        await self.redis.set(f"author_{author_id}", books_json, ex=60)

        return res