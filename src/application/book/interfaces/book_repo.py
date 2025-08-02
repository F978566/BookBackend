from abc import abstractmethod
from typing import List, Protocol
from uuid import UUID

from src.application.book.dto.book import BookDto
from src.domain.book.value_objects.book_status_enum import BookStatusEnum
from src.domain.book.entity import Book
from src.domain.book.entity import Page


class BookRepo(Protocol):
    @abstractmethod
    async def create_book(
        self,
        book: Book,
        author_id: UUID,
    ) -> None: ...

    @abstractmethod
    async def add_book_page(
        self,
        book_id: UUID,
        page: Page,
    ) -> None: ...

    @abstractmethod
    async def set_status(self, status: BookStatusEnum) -> bool: ...

    @abstractmethod
    async def add_redactor(self, book_id: UUID, redactor_id: UUID) -> bool: ...

    @abstractmethod
    async def add_author(self, book_id: UUID, author_id: UUID) -> bool: ...

    @abstractmethod
    async def get_all_books_by_author(self, author_id: UUID) -> List[BookDto]: ...
