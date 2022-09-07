import numpy as np

from .enums import RepeatMode
from .base import BaseAnimation


class BaseLinearAnimation(BaseAnimation):
    """
    Abstract base class for linear animations (no easing).

    Args:
        duration (int): Animation duration in milliseconds.
        step (int): Time interval between frames in milliseconds.
            Defaults to None.
        fps (int): Animation frame rate. Can be specified instead of `step`.
            Defaults to None.
        repeat (RepeatMode): Animation repeat mode.
            Defaults to RepeatMode.ONEOFF. See enum class for details.

    Raises:
        ValueError: If `step` and `fps` are set simultaneously.

    """

    def __init__(self, duration: int, step: int = None, fps: int = None,
                 repeat = RepeatMode.ONEOFF):
        super(BaseLinearAnimation, self).__init__(duration, step, fps, repeat)

    def _phi(self, dt: int) -> float:
        return np.clip(dt / self._duration, a_min=0, a_max=1).item()
