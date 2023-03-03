from dataclasses import dataclass, field

from uuid6 import UUID, uuid7

from dataclasses_asdict.dataclass_child import DataclassChild


@dataclass
class DataclassParent:
    id: UUID = field(default_factory=uuid7, init=False)
    name: str

    childs: dict[str, DataclassChild] = field(default_factory=dict, init=False)
