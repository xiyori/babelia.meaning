from typing import Sequence

from lib.math_utils import Point2D
from lib.utils import exported_image_exists, export_image, \
    print_exception, print_red, print_cyan
from lib.command import Command, ScaleParser, ColorParser, \
    ThicknessParser, TransparentParser


def export(response: Command, imgname: str,
           strokes: Sequence[Sequence[Point2D]]):
    """
    Export image command interface.

    Args:
        response (Command): User command.
        imgname (str): Background image name.
        strokes (:obj:`Sequence` of :obj:`Sequence` of :obj:`Point2D`):
            List of strokes to save.

    """
    try:
        (scale, color, thickness,
         transparent), args = response.parse_options(
            parsers=[ScaleParser(shortened=True, default=5), ColorParser(),
                     ThicknessParser(), TransparentParser()],
        )
        filename = args[0]
    except ValueError as e:
        print_exception(e)
        return
    except IndexError:
        print_red("Filename missing!")
        return

    if exported_image_exists(filename):
        print_cyan(f"Exported image \"{filename}\" already exists!")
        print("Overwrite? Y/N: ", end="")
        if input().lower() != "y":
            return

    try:
        export_image(filename, imgname, strokes,
                     scale, color, thickness, transparent)
        print(f"Succesfully exported \"{filename}\".")
    except BaseException as e:
        print_red(f"Cannot export \"{filename}\"!")
        print_exception(e)
