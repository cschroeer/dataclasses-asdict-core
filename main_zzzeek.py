from dataclasses import dataclass
from dataclasses import field
from dataclasses import asdict

from uuid import UUID
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Uuid
from sqlalchemy.orm import attribute_keyed_dict
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship


@dataclass
class DataclassChild:
    id: UUID = field(default_factory=uuid4, init=False)
    name: str


@dataclass
class DataclassParent:
    id: UUID = field(default_factory=uuid4, init=False)
    name: str

    childs: dict[str, DataclassChild] = field(default_factory=dict, init=False)


metadata: MetaData = MetaData()
mapper_registry: registry = registry(metadata=metadata)

dataclass_parent_table: Table = Table(
    "dataclass_parent",
    mapper_registry.metadata,
    Column("id", Uuid, primary_key=True),
    Column("name", String),
)

mapper_registry.map_imperatively(
    DataclassParent,
    dataclass_parent_table,
    properties={
        "childs": relationship(
            DataclassChild,
            collection_class=attribute_keyed_dict("name"),
        )
    },
)

dataclass_child_table: Table = Table(
    "dataclass_child",
    mapper_registry.metadata,
    Column("id", Uuid, primary_key=True),
    Column("name", String),
    Column(
        "dataclass_parent_id",
        Uuid,
        ForeignKey("dataclass_parent.id"),
    ),
)

mapper_registry.map_imperatively(DataclassChild, dataclass_child_table)

# added this just to check
mapper_registry.configure()


# Added from cschroeer: 
childs = {"child1": DataclassChild("child1"), "child2": DataclassChild("child2")}

parent = DataclassParent("parent1")
parent.childs = childs

# new compard to previous

asdict(parent)

#Traceback (most recent call last):
#  File "/home/cschroeer/python-projects/dataclasses-asdict-core/main_zzzeek.py", line 78, in <module>
#    asdict(parent)
#  File "/usr/local/lib/python3.10/dataclasses.py", line 1238, in asdict
#    return _asdict_inner(obj, dict_factory)
#  File "/usr/local/lib/python3.10/dataclasses.py", line 1245, in _asdict_inner
#    value = _asdict_inner(getattr(obj, f.name), dict_factory)
#  File "/usr/local/lib/python3.10/dataclasses.py", line 1275, in _asdict_inner
#    return type(obj)((_asdict_inner(k, dict_factory),
#TypeError: _mapped_collection_cls.<locals>._MKeyfuncMapped.__init__() takes 1 positional argument but 2 were given