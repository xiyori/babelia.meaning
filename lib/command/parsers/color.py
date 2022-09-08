from .base import BaseParser
from ..option import Option
from lib.math_utils import Point2D


class ColorParser(BaseParser):
    def __init__(self):
        super(ColorParser, self).__init__(
            name="color",
            mapping=None,
            default=(0, 0, 0),
            unwrapped=False
        )

    def __call__(self, option: Option) -> tuple:
        if option.name == self._name or option.name == self._name[0]:
            try:
                color = [int(c) for c in reversed(option.value.split(sep=","))]
                if len(color) != 3:
                    raise ValueError("wrong number of channels")
                return tuple(color)
            except BaseException:
                pass
        raise IndexError("no suitable conversion")
