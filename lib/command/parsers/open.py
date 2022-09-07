from .base import BaseParser
from lib.enums import OpenMode


class OpenParser(BaseParser):
    def __init__(self):
        super(OpenParser, self).__init__(
            name="mode",
            mapping={"normal": OpenMode.NORMAL,
                     "fast": OpenMode.FAST,
                     "draw": OpenMode.DRAW,
                     "bookmark": OpenMode.BOOKMARK},
            default=OpenMode.NORMAL
        )
