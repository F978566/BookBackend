from typing import List
from uuid import UUID, uuid4
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import UUID as SQLAlchemyUUID
from sqlalchemy.sql.schema import ForeignKey

from src.domain.book.value_objects.book_status_enum import BookStatusEnum
from src.infrastructure.db.models.user import UserModel

from .base import Base
from src.infrastructure.db.models.association_tables import redactors_book_association
from src.infrastructure.db.models.association_tables import auhtors_book_association


class BookModel(Base):
    __tablename__ = "book_model"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    title: Mapped[str]
    size: Mapped[int]
    pages: Mapped[List["PageModel"]] = relationship(back_populates="book")
    authors: Mapped[List["UserModel"]] = relationship(secondary=auhtors_book_association, back_populates="author_books")
    redactors: Mapped[List["UserModel"]] = relationship(secondary=redactors_book_association, back_populates="redactor_books")
    status: Mapped[BookStatusEnum] = mapped_column(Enum(BookStatusEnum), default=BookStatusEnum.IN_PROGRESS)



class PageModel(Base):
    __tablename__ = "page_model"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    text: Mapped[str]
    number: Mapped[int]
    book_id: Mapped[UUID] = mapped_column(ForeignKey("book_model.id"))
    book: Mapped["BookModel"] = relationship(back_populates="pages")
