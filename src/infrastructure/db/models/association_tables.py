from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey, Table

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
