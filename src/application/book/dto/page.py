from dataclasses import dataclass
from uuid import UUID

from src.application.dto import DTO


@dataclass(frozen=True)
class PageDto(DTO):
    id: UUID
    number: int
    text: str
