import numpy as np

from .enums import RepeatMode, EasingFunc
from .base import BaseAnimation


class BaseEasingAnimation(BaseAnimation):
    """
    Abstract base class for animations with quadratic easing.

    Formulas and graphs can be found at https://www.desmos.com/calculator/m6ntd0rbnn

    Args:
        duration (int): Animation duration in milliseconds.
        step (int): Time interval between frames in milliseconds.
            Defaults to None.
        fps (int): Animation frame rate. Can be specified instead of `step`.
            Defaults to None.
        repeat (RepeatMode): Animation repeat mode.
            Defaults to RepeatMode.ONEOFF. See enum class for details.
        easing (EasingFunc): Easing function.
            Defaults to EasingFunc.LINEAR. See enum class for details.

    Raises:
        ValueError: If `step` and `fps` are set simultaneously.

    """

    def __init__(self, duration: int, step: int = None, fps: int = None,
                 repeat = RepeatMode.ONEOFF, easing = EasingFunc.LINEAR):
        super(BaseEasingAnimation, self).__init__(duration, step, fps, repeat)
        self._easing = easing

        # Easing in/out
        self._t1 = min(250., self._duration)
        self._t2 = min(250., self._duration)

        self._a1 = 1 / (2 * self._t1 * self._duration - self._t1 ** 2)
        self._a2 = 1 / (2 * self._t2 * self._duration - self._t2 ** 2)

        # Smooth easing
        self._t3 = min(250., self._duration / 2)
        self._t4 = min(250., self._duration / 2)

        self._a3 = 1 / (2 * self._t3 * self._duration - self._t3 ** 2 - self._t3 * self._t4)
        self._a4 = 1 / (2 * self._t4 * self._duration - self._t4 ** 2 - self._t3 * self._t4)

        # Pulse in/out
        self._t5 = min(250., self._duration)
        self._t6 = min(250., self._duration)
        self._s = 1.2

        self._a5 = (1 + 2 * self._duration * (self._s - 1) / self._t5) / \
                   (self._t5 ** 2 - 3 * self._t5 * self._duration / 2)
        self._a6 = (1 + 2 * self._duration * (self._s - 1) / self._t6) / \
                   (self._t6 ** 2 - 3 * self._t6 * self._duration / 2)

        self._b5 = 2 * (self._a5 * (self._t5 ** 2 / 4 - self._t5 * self._duration) - self._s + 1) / self._t5
        self._b6 = 2 * (self._a6 * (self._t6 ** 2 / 4 - self._t6 * self._duration) - self._s + 1) / self._t6

        self._c5 = self._a5 * (self._duration - self._t5) ** 2
        self._c6 = self._a6 * (self._duration - self._t6) ** 2

    def _phi(self, dt: int) -> float:
        if self._easing == EasingFunc.LINEAR:
            return np.clip(dt / self._duration, a_min=0, a_max=1).item()
        elif self._easing == EasingFunc.IN:
            if dt < 0:
                return 0
            elif dt < self._t1:
                return self._a1 * dt ** 2
            else:
                return np.clip(2 * self._a1 * self._t1 * dt -
                               self._a1 * self._t1 ** 2, a_min=0, a_max=1).item()
        elif self._easing == EasingFunc.OUT:
            if dt < self._duration - self._t2:
                return np.clip(2 * self._a2 * self._t2 * dt, a_min=0, a_max=1).item()
            elif dt < self._duration:
                return 1 - self._a2 * (self._duration - dt) ** 2
            else:
                return 1
        elif self._easing == EasingFunc.SMOOTH:
            if dt < 0:
                return 0
            elif dt < self._t3:
                return self._a3 * dt ** 2
            elif dt < self._duration - self._t4:
                return 2 * self._a3 * self._t3 * dt - self._a3 * self._t3 ** 2
            elif dt < self._duration:
                return 1 - self._a4 * (self._duration - dt) ** 2
            else:
                return 1
        elif self._easing == EasingFunc.PULSEIN:
            if dt < 0:
                return 0
            elif dt < self._t5:
                return 1 - (self._a5 * (self._duration - dt) ** 2 +
                            self._b5 * (self._duration - dt) + self._c5)
            elif dt < self._duration:
                return 1 - (2 * self._a5 * (self._duration - self._t5) + self._b5) * (self._duration - dt)
            else:
                return 1
        elif self._easing == EasingFunc.PULSEOUT:
            if dt < 0:
                return 0
            elif dt < self._duration - self._t6:
                return (2 * self._a6 * (self._duration - self._t6) + self._b6) * dt
            elif dt < self._duration:
                return self._a6 * dt ** 2 + self._b6 * dt + self._c6
            else:
                return 1
