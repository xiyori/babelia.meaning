from .base import BaseParser


class IntersectParser(BaseParser):
    def __init__(self):
        super(IntersectParser, self).__init__(
            name=None,
            mapping={"intersect": True},
            default=False
        )
