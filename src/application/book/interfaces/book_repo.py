from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.application.book.dto.book import BookDto
from src.application.book.dto.page import PageDto
from src.domain.book.value_objects.book_status_enum import BookStatusEnum
from src.domain.book.entity import Book
from src.domain.book.entity import Page


class BookRepo(Protocol):
    @abstractmethod
    async def create_book(self, book: Book) -> BookDto: ...

    @abstractmethod
    async def add_book_page(
        self,
        book_id: UUID,
        page: Page,
    ) -> PageDto: ...

    @abstractmethod
    def set_status(self, status: BookStatusEnum) -> bool: ...

    @abstractmethod
    def add_redactor(self, redactor_id: UUID) -> bool: ...

    @abstractmethod
    def add_author(self, author_id: UUID) -> bool: ...
