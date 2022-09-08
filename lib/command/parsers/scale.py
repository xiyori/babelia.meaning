from .base_int_pos import BaseIntPosParser


class ScaleParser(BaseIntPosParser):
    def __init__(self, shortened: bool = False, default = None):
        super(ScaleParser, self).__init__(
            name="scale",
            default=default,
            shortened=shortened
        )
