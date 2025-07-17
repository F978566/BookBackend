from dataclasses import dataclass

from src.domain.common.value_object.value_object import ValueObject
from .book_status_enum import BookStatusEnum


@dataclass(frozen=True)
class BookStatus(ValueObject[BookStatusEnum]):
    value: BookStatusEnum = BookStatusEnum.IN_PROGRESS
