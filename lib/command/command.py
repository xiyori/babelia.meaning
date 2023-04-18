from typing import Optional, Sequence

from .option import Option
from .parsers import BaseParser


class Command(list):
    """
    Console command parser.

    Supports specifying options anywhere in the arguments,
    e.g. `command --option ARG` and `command ARG --option`
    will both produce the same results.

    Arguments can be separated by an arbitrary number of spaces.
    Double quotes can be used to escape spaces.

    Args:
        input (str): Command string.

    """

    def __init__(self, input: str):
        super(Command, self).__init__()
        begin = 0
        while begin < len(input):
            while begin < len(input) and input[begin] == " ":
                begin += 1
            if begin >= len(input):
                break
            elif input[begin] == "\"":
                begin += 1
                end = begin
                while end < len(input) and input[end] != "\"":
                    end += 1
                self.append(input[begin:end])
                begin = end + 1
            else:
                end = begin
                while end < len(input) and input[end] != " ":
                    end += 1
                self.append(input[begin:end])
                begin = end

    def option(self, index: int) -> Option:
        """
        Interpret command argument as an option.

        Args:
            index (int): Argument index.

        Returns:
            Option: Processed argument.

        Raises:
            ValueError: If the argument is not an option.

        """
        option: str = self[index]
        if option.startswith("--"):
            option = option[2:]
        elif option.startswith("-"):
            option = option[1:]
        else:
            raise ValueError(f"option \"{self[index]}\" not understood")
        end = 0
        while end < len(option) and option[end] != "=":
            end += 1
        if end >= len(option):
            return Option(option[:end])
        return Option(option[:end], option[end + 1:])

    def parse_options(self, parsers: Sequence[BaseParser],
                      n_args: Optional[int] = 1,
                      return_toggled: bool = False) -> tuple:
        """
        Process command arguments according to parsers.

        Args:
            parsers (:obj:`Sequence` of :obj:`BaseParser`):
                Command option parsers.
            n_args (:obj:`int`, optional): Maximum number of plain arguments.
                Defaults to 1. If set to None, any number of arguments
                that cannot be interpreted as options is allowed.
            return_toggled (bool): Whether to return an array indicating
                which parsers successfully processed an option.
                Defaults to False.

        Returns:
            list: Parsed option values.
            list: Plain arguments in the order of appearance.
            :obj:`list`, optional: Boolean array indicating which parsers
                successfully processed an option.

        Raises:
            ValueError: If more than `n_args` arguments cannot
                be processed as options.
            ValueError: If an option is set more than once.

        """
        values = [parser.default for parser in parsers]
        toggled = [False] * len(parsers)
        args = []
        for i in range(1, len(self)):
            try:
                option = self.option(i)
                option_found = False
                for j, parser in enumerate(parsers):
                    try:
                        values[j] = parser(option)
                        if toggled[j]:
                            raise ValueError("ambiguous options",
                                             "rethrow")
                        toggled[j] = True
                        option_found = True
                    except IndexError:
                        pass
                if not option_found:
                    raise ValueError(f"option \"{self[i]}\" not understood")
            except ValueError as e:
                if (n_args is not None and len(args) >= n_args) or len(e.args) > 1:
                    raise e
                else:
                    args.append(self[i])
        if return_toggled:
            return values, args, toggled
        return values, args

    @property
    def name(self) -> str:
        """
        Command name.

        """
        return self[0]

    @name.setter
    def name(self, value: str):
        self.insert(0, value)
