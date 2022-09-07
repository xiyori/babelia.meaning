import numpy as np

from .enums import RepeatMode, EasingFunc
from .base_easing import BaseEasingAnimation


class BaseFigureAnimation(BaseEasingAnimation):
    """
    Abstract base class for OpenCV figure animations.

    Args:
        start (dict): Starting params dictionary.
        finish (dict): Final params dictionary.
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

    def __init__(self, start: dict, finish: dict,
                 duration: int, step: int = None, fps: int = None,
                 repeat = RepeatMode.ONEOFF, easing = EasingFunc.LINEAR):
        super(BaseFigureAnimation, self).__init__(duration, step, fps, repeat, easing)
        self._from = start
        self._to = finish

    def _inter(self, phi: float) -> dict:
        """
        Interpolate between starting and final parameters.

        Use starting values for params with no final value present.

        Args:
            phi (float): Phi value.
                0 corresponds to animation start.
                1 corresponds to animation finish.

        Returns:
            dict: Interpolated params.

        """
        inter = dict()
        if "position" in self._to:
            pos_from = self._from["position"]
            pos_to = self._to["position"]
            inter["position"] = ((pos_from[0] + (pos_to[0] - pos_from[0]) * phi + 0.5).int(),
                                 (pos_from[1] + (pos_to[1] - pos_from[1]) * phi + 0.5).int())
        elif "position" in self._from:
            inter["position"] = self._from["position"]
        if "color" in self._to:
            col_from = np.array(self._from["color"])
            col_to = np.array(self._to["color"])
            inter["color"] = (col_from + (col_to - col_from) * phi + 0.5).astype(int).tolist()
        elif "color" in self._from:
            inter["color"] = self._from["color"]
        if "thickness" in self._to:
            thc_from = self._from["thickness"]
            thc_to = self._to["thickness"]
            inter["thickness"] = int(thc_from + (thc_to - thc_from) * phi + 0.5)
        elif "thickness" in self._from:
            inter["thickness"] = self._from["thickness"]
        return inter
