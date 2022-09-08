import sys
import colorama

from typing import Sequence

from lib import ui
from lib.math_utils import Point2D
from lib.utils import get_bookmarks, get_images, print_lib, print_red
from lib.enums import CommandNames
from lib.command import Command


imgname: str = None                          #: Last opened image name.
strokes: Sequence[Sequence[Point2D]] = None  #: The most recent editing results.

argv = sys.argv

colorama.init()  # Init colored console output

print_lib(get_bookmarks(), "bookmark", suff="b")
print_lib(get_images(), "image")

while True:
    if len(argv) > 1:
        response = Command(" ".join(argv[1:]))
        argv = []
    else:
        print("> ", end="")
        response = Command(input())
        if len(response) == 0:
            response.name = CommandNames.exit.value[0]

    if response.name in CommandNames.exit.value:
        print("\nProgram finished.")
        break
    elif response.name in CommandNames.help.value:
        ui.help(response)
    elif response.name in CommandNames.list.value:
        ui.list(response)
    elif response.name in CommandNames.bookmark.value:
        if strokes is None:
            print_red("Nothing to bookmark!")
        else:
            ui.bookmark(response, imgname, strokes)
    elif response.name in CommandNames.remove.value:
        ui.remove(response)
    elif response.name in CommandNames.export.value:
        if strokes is None:
            print_red("Nothing to export!")
        else:
            ui.export(response, imgname, strokes)
    else:
        if response.name not in CommandNames.open.value:
            response.name = CommandNames.open.value[0]

        result = ui.open(response)
        if isinstance(result, tuple):
            imgname, strokes = result
        else:
            imgname = None
            strokes = None
