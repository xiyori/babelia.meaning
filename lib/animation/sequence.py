import numpy as np

from typing import Sequence

from .enums import RepeatMode
from .base import BaseAnimation
from .base_linear import BaseLinearAnimation


class SequenceAnimation(BaseLinearAnimation):
    """
    Wrapper for playing several animations as a sequence.

    Internal animation frame rates are ignored and can be not set.

    Args:
        sequence (:obj:`Sequence` of :obj:`BaseAnimation`):
            Animations to display.
        timestamps (Sequence): Start times for corresponding animations.
            Defaults to succesive playback.
        step (int): Time interval between frames in milliseconds.
            Defaults to None.
        fps (int): Animation frame rate. Can be specified instead of `step`.
            Defaults to None.
        repeat (RepeatMode): Animation repeat mode.
            Defaults to RepeatMode.ONEOFF. See enum class for details.

    Raises:
        ValueError: If `step` and `fps` are set simultaneously.

    """

    def __init__(self, sequence: Sequence[BaseAnimation],
                 timestamps: Sequence = None,
                 step: int = None, fps: int = None,
                 repeat = RepeatMode.ONEOFF):
        durations = [animation.duration for animation in sequence]
        if timestamps is None:  # Play one by one
            timestamps = [0] + np.cumsum(durations[:-1])
        duration = np.max([t + d for t, d in zip(timestamps, durations)])
        super(SequenceAnimation, self).__init__(duration, step, fps, repeat)
        self._sequence = sequence
        self._timestamps = timestamps

    def _draw(self, phi: float, img: np.ndarray):
        time = int(phi * self._duration)
        for timestamp, animation in zip(self._timestamps, self._sequence):
            dt = time - timestamp
            if dt >= 0:
                animation.draw(dt, img)
