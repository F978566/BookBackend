from dataclasses import dataclass, field

from src.domain.common.entity.entity import Entity

@dataclass
class Page(Entity):
    number: int = field(default_factory=int)
    text: str = field(default_factory=str)

    @classmethod
    def create(
        cls,
        text: str,
        number: int,
    ) -> "Page":
        return Page(number=number, text=text)
