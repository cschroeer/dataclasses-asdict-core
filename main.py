from dataclasses import dataclass, field
from uuid import UUID, uuid4

from sqlalchemy import Column, ForeignKey, MetaData, String, Table, Uuid, inspection
from sqlalchemy.orm import attribute_keyed_dict, registry, relationship


@dataclass
class DataclassChild:
    id: UUID = field(default_factory=uuid4, init=False)
    name: str


@dataclass
class DataclassParent:
    id: UUID = field(default_factory=uuid4, init=False)
    name: str

    childs: dict[str, DataclassChild] = field(default_factory=dict, init=False)


def map_entities(schema_name: str = "dataclasses_asdict") -> registry:
    """Maps all model classes that should be stored in a database table to a database table via imperatively mapping from SQLAlchemy

    Args:
        schema_name (str, optional): The name of the database schema to map the model classes to. Defaults to "dataclasses_asdict".

    Returns:
        registry: The SQLAlchemy registry that contains all mapped tables.
                  Returning the registry is important if the tables in the registry should be crated in a database in a next step.
    """

    metadata: MetaData = MetaData(schema=schema_name)
    mapper_registry: registry = registry(metadata=metadata)

    if not inspection.inspect(DataclassParent, False):
        print("Map entity DataclassParent")
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
    else:
        print("Entity DataclassParent is already mapped")

    if not inspection.inspect(DataclassChild, False):
        print("Map entity DataclassChild")
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

    return mapper_registry


def create_parent():
    childs = {"child1": DataclassChild("child1"), "child2": DataclassChild("child2")}

    parent = DataclassParent("parent1")
    parent.childs = childs

    return parent


def test_dict(parent: DataclassParent):
    test_dict = dict(((k), (v)) for k, v in parent.childs.items())

    print(f"{test_dict=}")


def test_type(parent: DataclassParent):
    test_type = type(parent.childs)(((k), (v)) for k, v in parent.childs.items())

    print(f"{test_type=}")


# testing functions WITHOUT mapping
test_dict(create_parent())  # => works
test_type(create_parent())  # => works

# testing functions WITH mapping
map_entities()
test_dict(create_parent())  # => works
test_type(
    create_parent()
)  # => does not work TypeError: _mapped_collection_cls.<locals>._MKeyfuncMapped.__init__() takes 1 positional argument but 2 were given
