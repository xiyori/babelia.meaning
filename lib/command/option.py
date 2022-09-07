class Option:
    """
    Command option struct.

    Args:
        name (str): Option name.
        value (str): Option value. Defaults to None.

    """

    def __init__(self, name: str, value: str = None):
        self.name = name
        self.value = value
