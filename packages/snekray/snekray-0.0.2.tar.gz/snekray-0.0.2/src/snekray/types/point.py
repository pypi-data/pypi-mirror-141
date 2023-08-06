from __future__ import annotations
from typing import Union
from .ptuple import PTuple
import snekray


class Point(PTuple):
    __name__: str = "Point"
    W = 1.0

    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__(x, y, z)
        self.w = self.W

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and isinstance(other, Point)

    def __add__(self, tup: PTuple) -> Point:
        if isinstance(tup, snekray.Vector):
            return Point(*super().__add__(tup).dims)
        return self

    def __sub__(self, tup: PTuple) -> Union[snekray.Vector, Point]:
        new_dims = super().__sub__(tup).dims
        if isinstance(tup, Point):
            return snekray.Vector(*new_dims)
        else:
            return Point(*new_dims)
