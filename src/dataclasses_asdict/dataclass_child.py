from dataclasses import dataclass, field

from uuid6 import UUID, uuid7


@dataclass
class DataclassChild:
    id: UUID = field(default_factory=uuid7, init=False)
    name: str
