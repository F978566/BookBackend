from abc import abstractmethod
from typing import TypeVar
from typing_extensions import Protocol


DOMAIN_MODEL = TypeVar("DOMAIN_MODEL")
T = TypeVar("T")


class Mapper[DOMAIN_MODEL, T](Protocol):
    @abstractmethod
    def domain_to_dto(self, domain_model: DOMAIN_MODEL) -> T: ...

    @abstractmethod
    def dto_to_domain(self, model: T) -> DOMAIN_MODEL: ...
