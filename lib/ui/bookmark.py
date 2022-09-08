from typing import Sequence

from lib.utils import get_bookmarks, bookmark_exists, save_bookmark, \
    print_lib, print_exception, print_red, print_cyan
from lib.math_utils import Point2D, optimize_strokes
from lib.command import Command, BookmarkParser
from lib.enums import BookmarkMode


def bookmark(response: Command, imgname: str,
             strokes: Sequence[Sequence[Point2D]]):
    """
    Save bookmark command interface.

    Args:
        response (Command): User command.
        imgname (str): Bookmark image name.
        strokes (:obj:`Sequence` of :obj:`Sequence` of :obj:`Point2D`):
            List of strokes to save.

    """
    try:
        (mode, ), args = response.parse_options(
            parsers=[BookmarkParser()],
        )
        bmkname = args[0]
    except ValueError as e:
        print_exception(e)
        return
    except IndexError:
        print_red("Bookmark name missing!")
        return

    if bookmark_exists(bmkname):
        print_cyan(f"Bookmark \"{bmkname}\" already exists!")
        print("Overwrite? Y/N: ", end="")
        if input().lower() != "y":
            return

    if mode == BookmarkMode.OPTIMIZE:
        strokes = optimize_strokes(strokes)

    try:
        save_bookmark(bmkname, imgname, strokes)
    except BaseException as e:
        print_red(f"Cannot save \"{bmkname}\"!")
        print_exception(e)

    print_lib(get_bookmarks(reload=True), "bookmark", suff="b")
