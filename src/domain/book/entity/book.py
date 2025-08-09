from dataclasses import dataclass, field
from uuid import UUID

from src.domain.book.value_objects.book_status import BookStatus
from src.domain.book.value_objects.book_status_enum import BookStatusEnum
from src.domain.common.entity.agregate_root import AgregateRoot
from .page import Page
from ..event import BookCreated, PageAdded


@dataclass
class Book(AgregateRoot):
    title: str = field(default_factory=str)
    pages: list[Page] = field(default_factory=list[Page])
    size: int = field(default=0)
    authors: list[UUID] = field(default_factory=list[UUID])
    redactors: list[UUID] = field(default_factory=list[UUID])
    status: BookStatus = field(default_factory=BookStatus)

    @classmethod
    def create(
        cls,
        title: str,
        author: UUID,
        redactor: UUID,
    ) -> "Book":
        book = Book(title=title)

        book.record_event(
            BookCreated(
                title=title,
                author=author,
            )
        )

        return Book(title=title, authors=[author], redactors=[redactor])

    def add_page(self, page_numbrer: int, text: str):
        self.size += 1
        self.pages.append(Page.create(text, page_numbrer))
        self.record_event(
            PageAdded(
                page_numbrer=page_numbrer,
                text=text,
            )
        )

    def change_book_status(
        self,
        user_id: UUID,
        status: BookStatusEnum,
    ):
        if (status == BookStatusEnum.APROOVED) and (user_id not in self.redactors):
            raise ValueError()

        if (status == BookStatusEnum.DENIED) and (user_id in self.redactors):
            raise ValueError()

        if (status == BookStatusEnum.IN_PROGRESS) and (user_id not in self.authors):
            raise ValueError()

        if (status == BookStatusEnum.PUBLISHED) and (user_id not in self.authors):
            raise ValueError()

        self.status = BookStatus(status)

        return Book(
            id=self.id,
            title=self.title,
            authors=self.authors,
            size=self.size,
            pages=self.pages,
            redactors=self.redactors,
            status=BookStatus(status),
        )

    def add_redactor(self, redactor_id: UUID):
        self.redactors.append(redactor_id)

    def add_author(self, author_id: UUID):
        self.redactors.append(author_id)
