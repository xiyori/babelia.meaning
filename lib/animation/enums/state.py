from enum import Enum


class State(Enum):
    """
    Animation state enum.

    """

    READY    = 0  #: Initial state for created animation.
    ACTIVE   = 1  #: Animation is playing. This state is set in `BaseAnimation.advance`.
    FINISHED = 2  #: Animation has stopped, but continues to display according to repeat mode.
    DISABLED = 3  #: Animation is finished or interrupted, it will be removed soon.
