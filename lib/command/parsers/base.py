from typing import Optional

from ..option import Option


class BaseParser:
    """
    Base command option parser class.

    Supported option formats:
        - `--name=value`
        - `--name=v`
        - `-n=value`
        - `-n=v`
        - `--value`
        - `-v`

    Args:
        name (str): Option name.
        mapping (dict): Mapping from string option values into parsed values.
        default (object): Default option value. Defaults to None.
        unwrapped (bool): Whether to recognize '--value', '-v' formats.
            Defaults to True.
        shortened (bool): Whether to recognize '--name=v', '-n=v'... formats.
            Defaults to True.

    """

    def __init__(self, name: Optional[str], mapping: dict, default = None,
                 unwrapped: bool = True, shortened: bool = True):
        self._name = name
        self._mapping = mapping
        self._default = default
        self._unwrapped = unwrapped
        self._shortened = shortened

    def __call__(self, option: Option):
        """
        Parse option.

        Args:
            option (Option): Option to parse.

        Returns:
            object: Parsed value.

        Raises:
            IndexError: If option cannot be processed.

        """
        for key, value in self._mapping.items():
            if ((self._unwrapped and
                    (option.name == key or
                     (self._shortened and option.name == key[0]))) or
                    ((option.name == self._name or
                      (self._shortened and self._name is not None and
                       option.name == self._name[0])) and
                     (option.value == key or
                      (self._shortened and option.name == key[0])))):
                return value
        raise IndexError("no suitable conversion")

    @property
    def default(self):
        """
        Default option value.

        """
        return self._default
