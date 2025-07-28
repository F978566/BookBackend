from abc import ABC
from typing import Any, Generic, TypeVar

import didiator

QRes = TypeVar("QRes")


class Query[QRes](didiator.Request[QRes], ABC):
    pass


Q = TypeVar("Q", bound=Query[Any])


class QueryHandler(didiator.Handler[Q, QRes], ABC, Generic[Q, QRes]):
    pass
