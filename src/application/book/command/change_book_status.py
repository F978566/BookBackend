from dataclasses import dataclass
from uuid import UUID

from src.application.book.interfaces.book_repo import BookRepo
from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces.user_repo import UserRepo
from src.domain.book.value_objects.book_status_enum import BookStatusEnum
from src.domain.user.value_object.user_role_enum import UserRoleEnum


@dataclass
class ChangeBookStatus(Command[None]):
    book_id: UUID
    user_id: UUID
    status: BookStatusEnum


class ChangeBookStatusHandler(CommandHandler[ChangeBookStatus, None]):
    def __init__(
        self,
        book_repo: BookRepo,
        user_repo: UserRepo,
        uof: UnitOfWork,
    ):
        self.book_repo = book_repo
        self.user_repo = user_repo
        self.uof = uof

    async def __call__(self, request: ChangeBookStatus) -> None:
        user = await self.user_repo.get_user_by_id(request.user_id)
        book = await self.book_repo.get_book_by_id(request.book_id)

        print(request.status, BookStatusEnum.APROOVED, request.user_id, book.authors)

        if (request.status == BookStatusEnum.APROOVED) and (UserRoleEnum.MODERATOR not in user.user_role):
            raise ValueError()

        if (request.status == BookStatusEnum.DENIED) and (UserRoleEnum.MODERATOR not in user.user_role):
            raise ValueError()

        if (request.status == BookStatusEnum.IN_PROGRESS) and (request.user_id not in book.authors):
            raise ValueError()

        if (request.status == BookStatusEnum.PUBLISHED) and (request.user_id not in book.authors):
            raise ValueError()

        await self.book_repo.set_status(book_id=request.book_id, status=request.status)
        await self.uof.commit()
