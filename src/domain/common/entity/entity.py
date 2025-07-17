from dataclasses import dataclass, field
from uuid import UUID, uuid4
from abc import ABC


@dataclass
class Entity(ABC):
    id: UUID = field(default_factory=uuid4)
