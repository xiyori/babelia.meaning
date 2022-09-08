from .base import BaseParser


class TransparentParser(BaseParser):
    def __init__(self):
        super(TransparentParser, self).__init__(
            name=None,
            mapping={"transparent": True},
            default=False
        )
