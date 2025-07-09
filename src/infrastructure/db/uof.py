from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.interfaces.uow import UnitOfWork


class SQLAlchemyUoW(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self):
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            raise err

    async def rollback(self):
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            raise err
