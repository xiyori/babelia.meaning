from .base import BaseParser
from lib.enums import BookmarkMode


class BookmarkParser(BaseParser):
    def __init__(self):
        super(BookmarkParser, self).__init__(
            name="mode",
            mapping={"optimize": BookmarkMode.OPTIMIZE,
                     "preserve": BookmarkMode.PRESERVE_ORDER},
            default=BookmarkMode.PRESERVE_ORDER
        )
