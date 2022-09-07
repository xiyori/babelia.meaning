import numpy as np

from .base import BaseParser
from ..option import Option


class SpeedParser(BaseParser):
    def __init__(self):
        super(SpeedParser, self).__init__(
            name="speed",
            mapping=None,
            default=1,
            unwrapped=False,
            shortened=False
        )

    def __call__(self, option: Option) -> float:
        if option.name == self._name:
            try:
                return np.clip(float(option.value), a_min=0.1, a_max=10).item()
            except BaseException:
                pass
        raise IndexError("no suitable conversion")
