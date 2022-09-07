from typing import Sequence

from lib import utils
from lib.utils import get_bookmarks, bookmark_exists, \
    print_lib, print_exception, print_red, print_cyan
from lib.math_utils import optimize_strokes
from lib.command import Command, BookmarkParser
from lib.enums import BookmarkMode


def save_bookmark(response: Command, imgname: str,
                  strokes: Sequence[Sequence]):
    """
    Save bookmark command interface.

    Args:
        response (Command): User command.
        imgname (str): Bookmark image name.
        strokes (:obj:`Sequence` of :obj:`Sequence`):
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
    utils.save_bookmark(bmkname, imgname, strokes)

    print_lib(get_bookmarks(reload=True), "bookmark", suff="b")
