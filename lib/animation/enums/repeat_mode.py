from enum import Enum


class RepeatMode(Enum):
    """
    Animation repeat mode enum.

    """

    ONEOFF = 0  #: Play animation once and disable (hide) it.
    RETURN = 1  #: Play animation once and return to the initial position.
    STICK  = 2  #: Play animation once and continue displaying the last frame.
    REPEAT = 3  #: Repeat animation indefinitely.
    SWING  = 4  #: Play animation forward, then in reverse; continue displaying the initial position.
    CYCLE  = 5  #: Cycle animation forward and backward indefinitely.
