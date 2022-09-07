from enum import Enum


class OpenMode(Enum):
    """
    Open mode enum.

    See manuals/open.man for more details.

    """

    NORMAL   = 0  #: Perform nearest point walk (the default).
    FAST     = 1  #: Perform nearest point walk without animations.
    DRAW     = 2  #: Draw lines using pixels of the same color.
    BOOKMARK = 3  #: Display bookmark contents.
