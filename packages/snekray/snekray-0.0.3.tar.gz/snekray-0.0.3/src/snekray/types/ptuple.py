from __future__ import annotations
from typing import cast
import math


class PTuple:
    __name__: str = "PTuple"

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.dims = (self.x, self.y, self.z)

    def __eq__(self, other: object) -> bool:
        return all(math.isclose(*d) for d in zip(self.dims, cast(PTuple, other).dims))

    def __add__(self, tup: PTuple) -> PTuple:
        return PTuple(self.x + tup.x, self.y + tup.y, self.z + tup.z)

    def __sub__(self, tup: PTuple) -> PTuple:
        return PTuple(self.x - tup.x, self.y - tup.y, self.z - tup.z)

    def __neg__(self) -> PTuple:
        return PTuple(*(-dim for dim in self.dims))

    def __mul__(self, scalar: float) -> PTuple:
        return PTuple(*(dim * scalar for dim in self.dims))

    def __repr__(self) -> str:
        return f"{self.__name__}: ({self.x:.2f},{self.y:.2f},{self.z:.2f})"
