from .base_int_pos import BaseIntPosParser


class ThicknessParser(BaseIntPosParser):
    def __init__(self):
        super(ThicknessParser, self).__init__(
            name="thickness",
            shortened=False
        )
