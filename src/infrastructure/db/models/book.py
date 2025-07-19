from typing import List
from uuid import UUID, uuid4
from sqlalchemy import Column, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import UUID as SQLAlchemyUUID

from src.domain.book.value_objects.book_status_enum import BookStatusEnum
from src.infrastructure.db.models.user import UserModel

from .base import Base


auhtors_book_association = Table(
    "auhtors_book_association_model",
    Base.metadata,
    Column("book_model_id", ForeignKey("book_model.id"), primary_key=True),
    Column("user_model_id", ForeignKey("user_model.id"), primary_key=True),
)

redactors_book_association = Table(
    "redactors_book_association_model",
    Base.metadata,
    Column("book_model_id", ForeignKey("book_model.id"), primary_key=True),
    Column("user_model_id", ForeignKey("user_model.id"), primary_key=True),
)


class BookModel(Base):
    __tablename__ = "book_model"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    title: Mapped[str]
    size: Mapped[int]
    pages: Mapped[List["PageModel"]] = relationship(back_populates="book")
    authors: Mapped[List["UserModel"]] = relationship(back_populates="author_books")
    redactors: Mapped[List["UserModel"]] = relationship(back_populates="redactor_books")
    status: Mapped[BookStatusEnum] = mapped_column(Enum(BookStatusEnum), default=BookStatusEnum.IN_PROGRESS)



class PageModel(Base):
    __tablename__ = "page_model"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    text: Mapped[str]
    number: Mapped[str]
    book: Mapped["BookModel"] = relationship(back_populates="pages")
