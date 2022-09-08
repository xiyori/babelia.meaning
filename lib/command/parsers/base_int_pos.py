from .base import BaseParser
from ..option import Option


class BaseIntPosParser(BaseParser):
    """
    Base positive integer parser class.

    Supported option formats:
        - `--name=value`
        - `--name=v`
        - `-n=value`
        - `-n=v`

    Args:
        name (str): Option name.
        default (object): Default option value. Defaults to None.
        shortened (bool): Whether to recognize '--name=v', '-n=v' formats.
            Defaults to True.

    """

    def __init__(self, name: str, default = None, shortened: bool = True):
        super(BaseIntPosParser, self).__init__(
            name=name,
            mapping=None,
            default=default,
            unwrapped=False,
            shortened=shortened
        )

    def __call__(self, option: Option) -> int:
        if (option.name == self._name or
                (self._shortened and option.name == self._name[0])):
            try:
                return max(int(option.value), 1)
            except BaseException:
                pass
        raise IndexError("no suitable conversion")
