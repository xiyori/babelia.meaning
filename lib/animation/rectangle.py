import cv2
import numpy as np

from .enums import RepeatMode, EasingFunc
from .base_figure import BaseFigureAnimation


class RectangleAnimation(BaseFigureAnimation):
    """
    OpenCV rectangle animation.

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
        super(RectangleAnimation, self).__init__(start, finish, duration, step, fps, repeat, easing)

    def _draw(self, phi: float, img: np.ndarray):
        inter = self._inter(phi)
        cv2.rectangle(img, inter["position"][0].tuple, inter["position"][1].tuple,
                      color=inter["color"], thickness=inter["thickness"])


class RectanglePositionAnimation(RectangleAnimation):
    """
    OpenCV rectangle position animation.

    Args:
        start (tuple): Starting coords. Tuple of 2 math_utils.Point2D vectors.
        finish (tuple): Final coords. Tuple of 2 math_utils.Point2D vectors.
        color (tuple): Rectangle color in BGR format.
        thickness (int): Rectangle thickness.
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

    def __init__(self, start: tuple, finish: tuple, color: tuple, thickness: int,
                 duration: int, step: int = None, fps: int = None,
                 repeat = RepeatMode.ONEOFF, easing = EasingFunc.LINEAR):
        start = {"position": start,
                 "color": color,
                 "thickness": thickness}
        finish = {"position": finish}
        super(RectanglePositionAnimation, self).__init__(start, finish, duration, step, fps, repeat, easing)


class RectangleColorAnimation(RectangleAnimation):
    """
    OpenCV rectangle color animation.

    Args:
        start (tuple): Starting color in BGR format.
        finish (tuple): Final color in BGR format.
        position (tuple): Rectangle coords. Tuple of 2 math_utils.Point2D vectors.
        thickness (int): Rectangle thickness.
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

    def __init__(self, start: tuple, finish: tuple, position: tuple, thickness: int,
                 duration: int, step: int = None, fps: int = None,
                 repeat = RepeatMode.ONEOFF, easing = EasingFunc.LINEAR):
        start = {"position": position,
                 "color": start,
                 "thickness": thickness}
        finish = {"color": finish}
        super(RectangleColorAnimation, self).__init__(start, finish, duration, step, fps, repeat, easing)


class RectangleThicknessAnimation(RectangleAnimation):

    """
    OpenCV rectangle thickness animation.

    Args:
        start (int): Starting thickness.
        finish (int): Final thickness.
        position (tuple): Rectangle coords. Tuple of 2 math_utils.Point2D vectors.
        color (tuple): Rectangle color in BGR format.
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

    def __init__(self, start: int, finish: int, position: tuple, color: tuple,
                 duration: int, step: int = None, fps: int = None,
                 repeat = RepeatMode.ONEOFF, easing = EasingFunc.LINEAR):
        start = {"position": position,
                 "color": color,
                 "thickness": start}
        finish = {"thickness": finish}
        super(RectangleThicknessAnimation, self).__init__(start, finish, duration, step, fps, repeat, easing)
