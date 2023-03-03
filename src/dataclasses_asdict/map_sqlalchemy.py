import logging

from sqlalchemy import Column, ForeignKey, MetaData, String, Table, Uuid, inspection
from sqlalchemy.orm import attribute_keyed_dict, registry, relationship

from dataclasses_asdict.dataclass_child import DataclassChild
from dataclasses_asdict.dataclass_parent import DataclassParent

LOGGER = logging.getLogger(__name__)


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
        LOGGER.debug("Map entity DataclassParent")
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
        LOGGER.debug("Entity DataclassParent is already mapped")

    if not inspection.inspect(DataclassChild, False):
        LOGGER.debug("Map entity DataclassChild")
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
