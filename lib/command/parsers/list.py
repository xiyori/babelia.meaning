from .base import BaseParser
from lib.enums import ListMode


class ListParser(BaseParser):
    def __init__(self):
        super(ListParser, self).__init__(
            name=None,
            mapping={"bookmarks": ListMode.BOOKMARKS,
                     "images": ListMode.IMAGES,
                     "all": ListMode.ALL},
            default=ListMode.ALL
        )
