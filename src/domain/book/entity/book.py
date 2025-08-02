from dataclasses import dataclass, field
from uuid import UUID

from src.domain.book.value_objects.book_status import BookStatus
from src.domain.book.value_objects.book_status_enum import BookStatusEnum
from src.domain.user.value_object.user_role_enum import UserRoleEnum
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
    ) -> "Book":
        book = Book(title=title)

        book.record_event(
            BookCreated(
                title=title,
                author=author
            )
        )

        return Book(title=title, authors=[author])

    def add_page(self, page_numbrer: int, text: str):
        self.size += 1
        self.pages.append(Page.create(text, page_numbrer))
        self.record_event(
            PageAdded(
                page_numbrer=page_numbrer,
                text=text,
            )
        )

    def mark_as_published(self, user_id: UUID):
        if user_id not in self.authors:
            return

        self.status = BookStatus(BookStatusEnum.PUBLISHED)

    def mark_as_aprooved(self, user_role: UserRoleEnum):
        if user_role == UserRoleEnum.MODERATOR:
            return

        self.status = BookStatus(BookStatusEnum.APROOVED)

    def mark_as_denied(self, user_role: UserRoleEnum):
        if user_role == UserRoleEnum.MODERATOR:
            return

        self.status = BookStatus(BookStatusEnum.DENIED)

    def mark_as_in_progress(self, user_id: UUID):
        if user_id not in self.authors:
            return

        self.status = BookStatus(BookStatusEnum.IN_PROGRESS)

    def add_redactor(self, redactor_id: UUID):
        self.redactors.append(redactor_id)

    def add_author(self, author_id: UUID):
        self.redactors.append(author_id)
