from .base import BaseParser


class RemoveParser(BaseParser):
    def __init__(self):
        super(RemoveParser, self).__init__(
            name=None,
            mapping={"all": True},
            default=False
        )
