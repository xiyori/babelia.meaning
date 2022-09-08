import io
import os

from typing import Sequence

from lib.math_utils import Point2D


bookmarks_dir = "data/__bookmarks__/"
_bookmarks = None


def get_bookmarks(reload: bool = False) -> list:
    """
    Get bookmarks library.

    Args:
        reload (bool): Whether to reload library from disk.
            Defaults to False.

    Returns:
        list: Bookmarks library.

    """
    global _bookmarks
    if reload or _bookmarks is None:
        if not os.path.isdir(bookmarks_dir):
            os.mkdir(bookmarks_dir)
        _bookmarks = [name[:-4] for name in os.listdir(bookmarks_dir)
                      if name.lower().endswith(".bmk")]
        _bookmarks.sort()
    return _bookmarks


def get_bookmark_name(filename: str) -> str:
    """
    Convert bookmark index to filename if possible.

    Args:
        filename (str): Bookmark name or index.

    Returns:
        str: Bookmark name.

    """
    if filename[-1] == "b":
        try:
            file_id = int(filename[:-1])
            return get_bookmarks()[file_id]
        except (ValueError, IndexError):
            pass
    return filename


def bookmark_exists(bmkname: str) -> bool:
    """
    Check if a bookmark already exists on disk.

    Args:
        bmkname (str): Bookmark name.

    Returns:
        bool: True if a bookmark exists.

    """
    return os.path.isfile(bookmarks_dir + bmkname + ".bmk")


def open_bookmark(filename: str) -> tuple:
    """
    Read bookmark content.

    Args:
        filename (str): Bookmark name or index.

    Returns:
        str: Bookmark image name.
        :obj:`list` of :obj:`list`: List of strokes.

    Raises:
        FileNotFoundError: If a bookmark with a given name or
            index does not exist.

    """
    bmkname = get_bookmark_name(filename)

    if bookmark_exists(bmkname):
        file = io.open(bookmarks_dir + bmkname + ".bmk", mode="r")
        lines = file.readlines()
        file.close()
        imgname = lines[0][:-1]
        strokes = [[Point2D(*[int(crd) for crd in ps.split(sep=",")])
                    for ps in line.split(sep=" ")] for line in lines[1:]]
        return imgname, strokes
    raise FileNotFoundError(f"bookmark \"{bmkname}\" not found")


def save_bookmark(bmkname: str, imgname: str,
                  strokes: Sequence[Sequence[Point2D]]):
    """
    Save bookmark to disk.

    Args:
        bmkname (str): Bookmark name.
        imgname (str): Bookmark image name.
        strokes (:obj:`Sequence` of :obj:`Sequence` of :obj:`Point2D`):
            List of strokes to save.

    """
    file = io.open(bookmarks_dir + bmkname + ".bmk", mode="w")
    file.write(imgname + "\n")
    file.writelines([" ".join([str(p) for p in stroke]) + "\n"
                     for stroke in strokes])
    file.flush()
    file.close()


def remove_bookmark(bmkname: str):
    """
    Remove existing bookmark from disk.

    Args:
        bmkname (str): Bookmark name.

    Raises:
        FileNotFoundError: If a bookmark with a given name
            does not exist.

    """
    os.remove(bookmarks_dir + bmkname + ".bmk")
