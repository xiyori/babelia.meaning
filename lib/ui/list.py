from lib.utils import get_bookmarks, get_images, \
    print_lib, print_exception
from lib.command import Command, ListParser
from lib.enums import ListMode


def list(response: Command):
    """
    List command interface.

    Args:
        response (Command): User command.

    """
    try:
        mode = response.parse_options(
            parsers=[ListParser()],
            n_args=0
        )[0][0]
        if mode == ListMode.BOOKMARKS or mode == ListMode.ALL:
            print_lib(get_bookmarks(reload=True), "bookmark", suff="b")
        if mode == ListMode.IMAGES or mode == ListMode.ALL:
            print_lib(get_images(reload=True), "image")
    except ValueError as e:
        print_exception(e)
