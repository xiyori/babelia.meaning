import numpy as np

from numbers import Number
from typing import Union

from . import norms


class Point2D:
    """
    Geometric 2D point (vector).

    Args:
        x (Union[Number, tuple]): x coordinate or a tuple of (x, y).
            If x is a tuple, y coordinate is ignored.
        y (Number): y coordinate.

    """

    def __init__(self, x: Union[Number, tuple] = 0, y: Number = 0):
        if isinstance(x, tuple):
            self.x, self.y = x
        else:
            self.x = x
            self.y = y

    def __hash__(self):
        return hash(self.tuple)

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    def __add__(self, p):
        if isinstance(p, int) or isinstance(p, float) or isinstance(p, np.ndarray):
            return Point2D(self.x + p, self.y + p)
        elif isinstance(p, Point2D):
            return Point2D(self.x + p.x, self.y + p.y)
        raise ValueError(f"Point2D does not support operations with type \"{type(p)}\"")

    def __sub__(self, p):
        if isinstance(p, int) or isinstance(p, float) or isinstance(p, np.ndarray):
            return Point2D(self.x - p, self.y - p)
        elif isinstance(p, Point2D):
            return Point2D(self.x - p.x, self.y - p.y)
        raise ValueError(f"Point2D does not support operations with type \"{type(p)}\"")

    def __mul__(self, p):
        if isinstance(p, int) or isinstance(p, float) or isinstance(p, np.ndarray):
            return Point2D(self.x * p, self.y * p)
        elif isinstance(p, Point2D):
            return self.x * p.x + self.y * p.y
        raise ValueError(f"Point2D does not support operations with type \"{type(p)}\"")

    def __matmul__(self, p):
        if isinstance(p, Point2D):
            return self.x * p.y - self.y * p.x
        raise ValueError(f"Point2D does not support operations with type \"{type(p)}\"")

    def __truediv__(self, p):
        if isinstance(p, int) or isinstance(p, float) or isinstance(p, np.ndarray):
            return Point2D(self.x / p, self.y / p)
        elif isinstance(p, Point2D):
            return Point2D(self.x / p.x, self.y / p.y)
        raise ValueError(f"Point2D does not support operations with type \"{type(p)}\"")

    def __floordiv__(self, p):
        if isinstance(p, int) or isinstance(p, float) or isinstance(p, np.ndarray):
            return Point2D(self.x // p, self.y // p)
        elif isinstance(p, Point2D):
            return Point2D(self.x // p.x, self.y // p.y)
        raise ValueError(f"Point2D does not support operations with type \"{type(p)}\"")

    def __mod__(self, p):
        if isinstance(p, int) or isinstance(p, float) or isinstance(p, np.ndarray):
            return Point2D(self.x % p, self.y % p)
        elif isinstance(p, Point2D):
            return Point2D(self.x % p.x, self.y % p.y)
        raise ValueError(f"Point2D does not support operations with type \"{type(p)}\"")

    def __pow__(self, p, modulo=None):
        if isinstance(p, int) or isinstance(p, float) or isinstance(p, np.ndarray):
            return Point2D(pow(self.x, p, modulo), pow(self.y, p, modulo))
        elif isinstance(p, Point2D):
            return Point2D(pow(self.x, p.x, modulo), pow(self.x, p.y, modulo))
        raise ValueError(f"Point2D does not support operations with type \"{type(p)}\"")

    def __round__(self, n=None):
        return Point2D(round(self.x, n), round(self.y, n))

    def __repr__(self):
        return f"Point2D({self.x}, {self.y})"

    def __str__(self):
        return f"{self.x},{self.y}"

    @property
    def tuple(self):
        return self.x, self.y

    def int(self):
        return Point2D(int(self.x), int(self.y))

    def norm(self, norm=norms.l2_norm):
        return norm(self.x, self.y)
