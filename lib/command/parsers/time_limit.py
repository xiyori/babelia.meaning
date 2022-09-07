from .base import BaseParser
from ..option import Option


class TimeLimitParser(BaseParser):
    def __init__(self):
        super(TimeLimitParser, self).__init__(
            name="time_limit",
            mapping=None,
            default=500,
            unwrapped=False
        )

    def __call__(self, option: Option) -> int:
        if option.name == self._name or option.name == self._name[0]:
            try:
                return max(int(option.value), 0)
            except BaseException:
                pass
        raise IndexError("no suitable conversion")
