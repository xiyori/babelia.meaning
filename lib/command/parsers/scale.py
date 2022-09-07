import numpy as np

from .base import BaseParser
from ..option import Option


class ScaleParser(BaseParser):
    def __init__(self):
        super(ScaleParser, self).__init__(
            name="scale",
            mapping=None,
            unwrapped=False,
            shortened=False
        )

    def __call__(self, option: Option) -> int:
        if option.name == self._name:
            try:
                return np.clip(int(option.value), a_min=1, a_max=10).item()
            except BaseException:
                pass
        raise IndexError("no suitable conversion")
