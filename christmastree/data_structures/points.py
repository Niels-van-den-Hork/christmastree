from __future__ import annotations
import math
from typing import Any, NamedTuple

PI = 3.14159

class Point2D_Base(NamedTuple):
    x: Any
    y: Any

    def get_distance(self, point : Point2D_Base) -> float:
        return math.sqrt((self.x-point.x)**2 + (self.y-point.y)**2)

class Point2D(Point2D_Base):  # refers to a x,y pixel (so intergers)
    x: int
    y: int

    def invert_y(self, image_height: int) -> Point2D:
        return Point2D(self.x, image_height - self.y)


    @classmethod
    @property
    def ZERO(cls):
        return cls(0, 0)

    


class Point2D_Float(Point2D_Base):  # refers to a x,y pixel (so intergers)
    x: float
    y: float


class ProjectedPoint(Point2D_Base):  # refers to a x,y pixel (so intergers)
    phi: float
    y: float


class Point3D(NamedTuple):  # refers to a x,y,z coordinate (so floats)
    x: float
    y: float
    z: float

    def __sub__(self, point: Point3D) -> Point3D:
        return Point3D(self.x - point.x, self.y - point.y, self.z - point.z)

    def __floordiv__(self, point: Point3D) -> Point3D:
        return Point3D(
            int(self.x / point.x), int(self.y / point.y), int(self.z / point.z)
        )

    def get_distance(self, point: Point3D):
        return math.sqrt(
            (self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2
        )

    @classmethod
    @property
    def ZERO(cls):
        return cls(0, 0, 0)

    @property
    def phi(self) -> float:
        """Returns the angle of the point compared to the origin."""
        return math.atan2(self.z, self.x)

    @property
    def corrected_phi(self) -> float:
        """Returns the angle of the point compared to the origin."""
        return _calculate_new_phi(self.phi, self.z)


def _calculate_new_phi(phi: float, z: float) -> float:
    #duplicates code from mocktree
    MIN_LAYER = 1
    MAX_LAYER = 9
    MAX_RADIUS = 2
    TOTAL_LAYERS = MAX_LAYER - MIN_LAYER

    def safe_div(a, b):
        if b == 0:
            return 0
        else:
            return a / b

    def _get_radius_at_layer(layer: float) -> float:
        if not (MIN_LAYER <= layer <= MAX_LAYER):
            raise ValueError("layer not in range [MIN_LAYER,MAX_LAYER]")

        return MAX_RADIUS - (layer - 1) / 4

    def _correction(layer):
        if not (MIN_LAYER <= layer <= MAX_LAYER):
            raise ValueError("layer not in range [MIN_LAYER,MAX_LAYER]")

        return 1 + (layer * TOTAL_LAYERS / PI)

    return safe_div((phi - (PI / 2)), (_get_radius_at_layer(z))) * _correction(z)