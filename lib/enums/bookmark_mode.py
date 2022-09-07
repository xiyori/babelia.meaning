from enum import Enum


class BookmarkMode(Enum):
    """
    Bookmark save mode enum.

    See manuals/bookmark.man for more details.

    """

    PRESERVE_ORDER = 0  #: Perform stroke optimization using graph algorithm.
    OPTIMIZE       = 1  #: Leave strokes as is (the default).
