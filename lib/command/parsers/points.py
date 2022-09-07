from .base import BaseParser


class PointsParser(BaseParser):
    def __init__(self):
        super(PointsParser, self).__init__(
            name=None,
            mapping={"points_disable": True},
            default=False
        )
