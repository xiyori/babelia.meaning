from enum import Enum


class MagnetState(Enum):
    """
    Editor magnet state enum.

    """

    STANDBY = 0  #: Magnet is not active.
    APPEND  = 1  #: A new point is ready to be added to the current stroke (not used).
    REMOVE  = 2  #: The last point is ready to be removed from the current stroke.
