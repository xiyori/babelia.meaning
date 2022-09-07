from lib import utils
from lib.utils import get_bookmarks, get_bookmark_name, \
    print_lib, enclose_quotes, print_exception, print_red
from lib.command import Command, RemoveParser


def remove_bookmark(response: Command):
    """
    Remove bookmark command interface.

    Args:
        response (Command): User command.

    """
    try:
        (remove_all, ), args = response.parse_options(
            parsers=[RemoveParser()],
            n_args=None
        )
    except ValueError as e:
        print_exception(e)
        return

    if remove_all:
        bmknames = get_bookmarks()

        if len(bmknames) == 0:
            print_red("Nothing to remove!")
            return
    else:
        bmknames = []
        for filename in args:
            bmkname = get_bookmark_name(filename)
            if bmkname not in bmknames:
                bmknames.append(bmkname)

        if len(bmknames) == 0:
            print_red("Bookmark names missing!")
            return

    print("Are you sure you want to delete following bookmarks: ",
          " ".join(enclose_quotes(bmknames)),
          "?", sep="")
    print("Y/N: ", end="")
    if input().lower() == "y":
        removed = []
        for bmkname in bmknames:
            try:
                utils.remove_bookmark(bmkname)
                removed.append(bmkname)
            except BaseException:
                print_red(f"Cannot delete \"{bmkname}\"!")

        if len(removed) > 0:
            print("Succesfully deleted ",
                  " ".join(enclose_quotes(removed)),
                  ".", sep="")
            print_lib(get_bookmarks(reload=True), "bookmark", suff="b")
