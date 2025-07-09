from abc import ABC
from typing import Any, Generic, TypeVar

import didiator

CRes = TypeVar("CRes")


class Command[CRes](didiator.Request[CRes], ABC):
    pass


C = TypeVar("C", bound=Command[Any])


class CommandHandler(didiator.Handler[C, CRes], ABC, Generic[C, CRes]):
    pass
