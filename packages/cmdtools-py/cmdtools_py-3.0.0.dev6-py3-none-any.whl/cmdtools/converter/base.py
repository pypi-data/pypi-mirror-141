from typing import Union

__all__ = [
    "BaseConverter",
    "BasicTypes",
]

BasicTypes = Union[int, float, str, bool]


class BaseConverter:
    def __init__(self, value: BasicTypes):
        self.value = value
