from abc import ABC
from typing import Any, Generic, TypeVar

import didiator

CRes = TypeVar("CRes")


class Command[CRes](didiator.Command[CRes], ABC):
    pass


C = TypeVar("C", bound=Command[Any])


class CommandHandler(didiator.CommandHandler[C, CRes], ABC, Generic[C, CRes]):
    pass
