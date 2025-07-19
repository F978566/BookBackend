from dataclasses import dataclass
from uuid import UUID

from application.dto import DTO
from domain.book.value_objects.book_status_enum import BookStatusEnum
from src.application.book.dto.page import PageDto


@dataclass(frozen=True)
class BookDto(DTO):
    id: UUID
    title: str
    pages: list[PageDto]
    size: int
    authors: list[UUID]
    redactors: list[UUID]
    status: BookStatusEnum
