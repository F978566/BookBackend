from abc import abstractmethod
from typing_extensions import Protocol


class UnitOfWork(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...
    
    @abstractmethod
    async def rollback(self) -> None: ...