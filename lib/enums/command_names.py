from enum import Enum


class CommandNames(Enum):
    """
    Console command names enum.

    """

    exit =     ["exit"]
    help =     ["help", "man"]
    list =     ["list", "ls"]
    bookmark = ["bookmark", "bm"]
    remove =   ["remove", "rm"]
    open =     ["open"]
