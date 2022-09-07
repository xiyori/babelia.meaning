from enum import Enum


class ListMode(Enum):
    """
    Library display mode enum.

    See manuals/list.man for more details.

    """

    BOOKMARKS = 0  #: Display bookmarks library.
    IMAGES    = 1  #: Display images library.
    ALL       = 2  #: Display full library (the default).
