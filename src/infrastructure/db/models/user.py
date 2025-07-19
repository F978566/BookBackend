from typing import List
from uuid import UUID, uuid4
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import UUID as SQLAlchemyUUID

# from infrastructure.db.models.book import BookModel
from src.domain.user.value_object.user_role_enum import UserRoleEnum

from .base import Base


class UserModel(Base):
    __tablename__ = "user_model"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    user_role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum))
    deleted: Mapped[bool]

    author_books: Mapped[List["BookModel"]] = relationship(back_populates="authors")
    redactor_books: Mapped[List["BookModel"]] = relationship(back_populates="redactors")

    def __repr__(self):
        return (f"UserModel(id={self.id!r}, "
                f"username={self.username!r}, "
                f"email={self.email!r}, "
                f"user_role={self.user_role!r}, "
                f"deleted={self.deleted!r})")
