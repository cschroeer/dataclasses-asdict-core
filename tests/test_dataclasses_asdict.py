import logging
from dataclasses import asdict

from dataclasses_asdict.dataclass_child import DataclassChild
from dataclasses_asdict.dataclass_parent import DataclassParent
from dataclasses_asdict.map_sqlalchemy import map_entities


def test_dataclass_asdict():
    childs = {"child1": DataclassChild("child1"), "child2": DataclassChild("child2")}

    parent = DataclassParent("parent1")
    parent.childs = childs

    parent_dict = asdict(parent)

    logging.debug(f"{parent_dict=}")

    pass


def test_dataclass_asdict_mapsqlalchemy():
    map_entities()

    childs = {"child1": DataclassChild("child1"), "child2": DataclassChild("child2")}

    parent = DataclassParent("parent1")
    parent.childs = childs

    parent_dict = asdict(parent)

    logging.debug(f"{parent_dict=}")

    pass
