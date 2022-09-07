import io


manuals_dir = "manuals/"
_manuals = dict()


def get_manual(name: str = "general") -> str:
    """
    Get command manual.

    Args:
        name (str): Command manual name.
            Defaults to "general".

    Returns:
        str: Command manual.

    """
    if name not in _manuals:
        file = io.open(manuals_dir + name + ".man", mode="r")
        _manuals[name] = "".join(file.readlines())
        file.close()
    return _manuals[name]
