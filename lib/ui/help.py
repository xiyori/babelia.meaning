from lib.enums import CommandNames
from lib.utils import get_manual, print_red
from lib.command import Command


def help(response: Command):
    """
    Help command interface.

    Args:
        response (Command): User command.

    """
    if len(response) < 2:
        print(get_manual())
    elif len(response) > 2:
        print_red("Too many arguments!")
    else:
        for command in CommandNames:
            if response[1] in command.value:
                print(get_manual(command.value[0]))
                return
        print_red(f"No manual entry for \"{response[1]}\"!")
