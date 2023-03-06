from dataclasses import field, asdict, dataclass


class MyDict(dict):

    def __init__(self):
        pass

    """Assume this does something useful"""
    def __repr__(self):
        original_repr = super().__repr__()
        return f"MyDict({original_repr})"

@dataclass
class X:
    x: MyDict = field(default_factory=MyDict)


inst = X()
inst.x["Key"] = "value"

converted = asdict(inst, dict_factory=MyDict)

print(f"{converted=}")