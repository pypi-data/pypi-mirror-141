from __future__ import annotations
from re import A
from typing import Optional, Union
import math

import snekray
from .ptuple import PTuple


class Vector(PTuple):
    W = 0.0
    __name__: str = "Vector"
    _normalized: Optional[Vector] = None

    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__(x, y, z)
        self.w = self.W

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and isinstance(other, Vector)

    def __add__(self, tup: PTuple) -> Union[Vector, snekray.Point]:
        new_dims = super().__add__(tup).dims
        if isinstance(tup, Vector):
            return Vector(*new_dims)
        else:
            return snekray.Point(*new_dims)

    def __sub__(self, tup: PTuple) -> Vector:
        if isinstance(tup, Vector):
            return Vector(*super().__sub__(tup).dims)
        return self

    def __neg__(self) -> Vector:
        return Vector(*super().__neg__().dims)

    def __mul__(self, scalar: float) -> Vector:
        return Vector(*super().__mul__(scalar).dims)

    def magnitude(self) -> float:
        return math.sqrt(sum((math.pow(dim, 2) for dim in self.dims)))

    def normalize(self) -> Vector:
        magnitude = self.magnitude()
        if self._normalized is not None:
            return self._normalized
        else:
            self._normalized = Vector(*(dim / magnitude for dim in self.dims))
            return self._normalized

    def dot(self, other: Vector) -> float:
        return sum(x * y for x, y in zip(self.dims, other.dims))

    def cross(self, other: Vector) -> Vector:
        x = (self.y * other.z) - (self.z * other.y)
        y = (self.z * other.x) - (self.x * other.z)
        z = (self.x * other.y) - (self.y * other.x)

        return Vector(x, y, z)
