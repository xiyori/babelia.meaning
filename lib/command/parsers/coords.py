from .base import BaseParser
from ..option import Option
from lib.math_utils import Point2D


class CoordsParser(BaseParser):
    def __init__(self):
        super(CoordsParser, self).__init__(
            name="coords",
            mapping=None,
            unwrapped=False
        )

    def __call__(self, option: Option) -> Point2D:
        if option.name == self._name or option.name == self._name[0]:
            try:
                return Point2D(*[int(crd) for crd in option.value.split(sep=",")])
            except BaseException:
                pass
        raise IndexError("no suitable conversion")
