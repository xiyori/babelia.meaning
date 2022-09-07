import numpy as np

from typing import Sequence

from .enums import RepeatMode
from .base import BaseAnimation
from .base_linear import BaseLinearAnimation


class ParallelAnimation(BaseLinearAnimation):
    """
    Wrapper for playing several animations at the same time.

    Internal animation frame rates are ignored and can be not set.

    Args:
        animations (:obj:`Sequence` of :obj:`BaseAnimation`):
            Animations to display.
        step (int): Time interval between frames in milliseconds.
            Defaults to None.
        fps (int): Animation frame rate. Can be specified instead of `step`.
            Defaults to None.
        repeat (RepeatMode): Animation repeat mode.
            Defaults to RepeatMode.ONEOFF. See enum class for details.

    Raises:
        ValueError: If `step` and `fps` are set simultaneously.

    """

    def __init__(self, animations: Sequence[BaseAnimation],
                 step: int = None, fps: int = None,
                 repeat = RepeatMode.ONEOFF):
        # Duration is a maximum among provided animations
        duration = np.max([animation.duration for animation in animations])
        super(ParallelAnimation, self).__init__(duration, step, fps, repeat)
        self._animations = animations

    def _draw(self, phi: float, img: np.ndarray):
        dt = int(phi * self._duration)
        for animation in self._animations:
            animation.draw(dt, img)
