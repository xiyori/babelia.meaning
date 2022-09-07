from termcolor import colored
from typing import Sequence


def print_lib(lib: Sequence, name: str, suff: str = ""):
    """
    Print library to console.

    Args:
        lib (Sequence): Library contents.
        name (str): Library name.
        suff (str): Index suffix.

    """
    print()
    if len(lib) == 0:
        print(colored(f"{name[0].upper()}{name[1:]}", "cyan"),
              "library empty.")
        return
    print(*[(colored("%4d%s" % (id, suff), "green") + " - \"%s\"" % name)
            for id, name in enumerate(lib)], sep=", ")
    print(f"Use index or filename to access {colored(name, 'cyan')}.")


def print_exception(e: BaseException):
    """
    Print error message to console.

    Args:
        e (BaseException): Error object.

    """
    print_red(e.args[0][0].upper() + e.args[0][1:] + "!")


def enclose_quotes(lib: Sequence) -> list:
    return [f"\"{name}\"" for name in lib]


def print_red(text: str):
    print(colored(text, "red"))


def print_green(text: str):
    print(colored(text, "green"))


def print_cyan(text: str):
    print(colored(text, "cyan"))
