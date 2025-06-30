from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        pass


@dataclass(frozen=True)
class ValueObject(ABC, Generic[T]):
    value: T
    
    def to_raw(self) -> T:
        return self.value
