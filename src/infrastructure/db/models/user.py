from typing import List
from uuid import UUID, uuid4
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import UUID as SQLAlchemyUUID

# from infrastructure.db.models.book import BookModel
from src.domain.user.value_object.user_role_enum import UserRoleEnum
from src.infrastructure.db.models.association_tables import redactors_book_association
from src.infrastructure.db.models.association_tables import auhtors_book_association

from .base import Base


class UserModel(Base):
    __tablename__ = "user_model"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    user_role: Mapped[List[UserRoleEnum]] = mapped_column(ARRAY(Enum(UserRoleEnum)))
    deleted: Mapped[bool]

    author_books: Mapped[List["BookModel"]] = relationship(secondary=auhtors_book_association, back_populates="authors")  # type: ignore # noqa: F821
    redactor_books: Mapped[List["BookModel"]] = relationship(secondary=redactors_book_association, back_populates="redactors")  # type: ignore # noqa: F821

    def __repr__(self):
        return (f"UserModel(id={self.id!r}, "
                f"username={self.username!r}, "
                f"email={self.email!r}, "
                f"user_role={self.user_role!r}, "
                f"deleted={self.deleted!r})")
