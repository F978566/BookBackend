import json
from typing import List
from uuid import UUID
from redis.asyncio import Redis # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import update, select
from sqlalchemy.orm import selectinload, attributes
from sqlalchemy import func
import dataclasses

from src.application.common.interfaces.db_model_mapper import DbModelMapper
from src.domain.user.value_object.user_role_enum import UserRoleEnum
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
        redis: Redis, # type: ignore
    ):
        self._session = session
        self._book_mapper = book_mapper
        self.redis = redis # type: ignore

    async def create_book(
        self,
        book: Book,
        author_id: UUID,
    ) -> UUID:
        new_book_model = BookModel(
            title=book.title,
            size=book.size,
        )
        self._session.add(new_book_model)
        await self._session.flush()

        author = (await self._session.execute(
            select(UserModel)
            .where(UserModel.id == author_id)
            .where(UserModel.user_role.contains([UserRoleEnum.WRITER.name.upper()])) # type: ignore
            .options(selectinload(UserModel.author_books)) # type: ignore
        )).scalar()
        author.author_books.append(new_book_model) # type: ignore

        moderator = (await self._session.execute(
            select(UserModel)
            .join(UserModel.redactor_books, isouter=True) # type: ignore
            .where(UserModel.user_role.contains([UserRoleEnum.MODERATOR]))
            .group_by(UserModel.id)
            .order_by(func.count(BookModel.id)) # Use BookModel.id for the count on the joined table
            .options(selectinload(UserModel.redactor_books)) # type: ignore
            .limit(1)
        )).scalar()

        moderator.redactor_books.append(new_book_model) # type: ignore

        return new_book_model.id

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

    async def set_status(self, book_id: UUID, status: BookStatusEnum) -> bool:
        try:
            await self._session.execute(
                update(BookModel)
                .where(BookModel.id == book_id)
                .values(status=status)
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
        cached_books = await self.redis.get(f"author_{author_id}") # type: ignore

        if cached_books:
            books_data = json.loads(cached_books) # type: ignore
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


        await self.redis.set(f"author_{author_id}", books_json, ex=60) # type: ignore

        return res

    async def choose_redactor(self) -> UUID:
        moderator = (await self._session.execute(
        select(UserModel.id)
            .join(UserModel.redactor_books, isouter=True) # type: ignore
            .where(UserModel.user_role.contains([UserRoleEnum.MODERATOR]))
            .group_by(UserModel.id)
            .order_by(func.count(BookModel.id)) # Use BookModel.id for the count on the joined table
            .limit(1)
        )).scalar()

        # book = (await self._session.execute(
        #     select(BookModel)
        #     .where(BookModel.id == book_id)
        # )).scalar_one_or_none()

        # moderator.redactor_books.append(book) # type: ignore

        return moderator # type: ignore

    async def get_book_by_id(self, book_id: UUID) -> BookDto:
        book = (await self._session.execute(
            select(BookModel)
            .where(BookModel.id == book_id)
            .options(
                selectinload(BookModel.authors), # type: ignore
                selectinload(BookModel.redactors), # type: ignore
                selectinload(BookModel.pages), # type: ignore
            )
        )).scalar_one_or_none()

        if book is None:
            raise ValueError()

        return self._book_mapper.db_model_to_dto(book)
