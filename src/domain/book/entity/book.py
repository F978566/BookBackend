from dataclasses import dataclass, field

from src.domain.common.entity.agregate_root import AgregateRoot
from .page import Page
from ..event import BookCreated, PageAdded
from uuid import UUID


@dataclass
class Book(AgregateRoot):
    title: str = field(default_factory=str)
    pages: list[Page] = field(default_factory=list)
    size: int = field(default=0)
    authors: list[UUID] = field(default_factory=list)
    redactors: list[UUID] = field(default_factory=list)
    published: bool = field(default=False)
    aprooved: bool = field(default=False)

    @classmethod
    def create(
        cls,
        title: str,
        author: UUID,
    ) -> "Book":
        book = Book(title=title)

        book.record_event(
            BookCreated(
                title=title,
                author=author
            )
        )

        return Book(title=title)

    def add_page(self, page_numbrer: int, text: str):
        self.size += 1
        self.pages.append(Page.create(text, page_numbrer))
        self.record_event(
            PageAdded(
                page_numbrer=page_numbrer,
                text=text,
            )
        )

    def publish(self):
        self.published = True

    def aproove(self):
        self.aprooved = True

    def add_redactor(self, redactor_id: UUID):
        self.redactors.append(redactor_id)

    def add_author(self, author_id: UUID):
        self.redactors.append(author_id)
