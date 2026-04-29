from abc import ABC, abstractmethod
from typing import Any, AsyncIterator


class BaseMessageBroker(ABC):
    @abstractmethod
    async def start(self): ...

    @abstractmethod
    async def close(self): ...

    @abstractmethod
    async def send_message(self, topic: str, value: bytes): ...

    @abstractmethod
    async def start_consuming(self, topic: str) -> AsyncIterator[dict[Any, Any]]: ...

    @abstractmethod
    async def stop_consuming(self, topic: str): ...
