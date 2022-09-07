import numpy as np

from lib.animation import BaseAnimation, ParallelAnimation, RectanglePositionAnimation, \
    LineAnimation, LinePositionAnimation, LineThicknessAnimation, \
    RepeatMode, EasingFunc
from lib.math_utils import metrics, Point2D


fps = 60                      #: Animations frame rate.

scale: int = None             #: Image scaling param.
line_thickness: int = None    #: Line thickness.
border_thickness: int = None  #: Point animation border thickness.
img: np.ndarray = None        #: Current original image.

l2_metric = metrics.L2Metric()


def point_appear(p: Point2D, stretch: int = 3, duration: int = 250,
                 reverse: bool = False) -> BaseAnimation:
    """
    Image pixel enlarge animation.

    Args:
        p (Point2D): Rectangle center.
        stretch (int): Number of pixels to extend in each direction.
            Defaults to 3. Rectangle size is `stretch` * 2 + 1.
        duration (int): Animation duration in ms.
            Defaults to 250 ms.
        reverse (bool): Whether to reverse the animation.
            Defaults to False.

    Returns:
        BaseAnimation: Point appear animation.

    """
    animation = ParallelAnimation(
        [RectanglePositionAnimation(
            start=(p * scale, (p + 1) * scale),
            finish=((p - stretch) * scale,
                    (p + 1 + stretch) * scale),
            color=img[p.y, p.x].tolist(),
            thickness=-1,
            duration=duration,
            repeat=RepeatMode.STICK,
            easing=EasingFunc.PULSEOUT
        ), RectanglePositionAnimation(
            start=(p * scale - border_thickness // 2,
                   (p + 1) * scale + border_thickness // 2),
            finish=((p - stretch) * scale - border_thickness // 2,
                    (p + 1 + stretch) * scale + border_thickness // 2),
            color=(255, 255, 255),
            thickness=border_thickness,
            duration=duration,
            repeat=RepeatMode.STICK,
            easing=EasingFunc.PULSEOUT
        )],
        fps=fps,
        repeat=RepeatMode.STICK
    )
    if reverse:
        animation.repeat = RepeatMode.ONEOFF
        animation.reverse()
    return animation


def point_pulse(p: Point2D, stretch_from: int = 3, stretch_to: float = 4,
                duration: int = 125) -> BaseAnimation:
    """
    Enlarged image pixel pulse animation.

    Args:
        p (Point2D): Rectangle center.
        stretch_from (int): Starting rectangle size param.
            Defaults to 3. Rectangle size is `stretch_from` * 2 + 1.
        stretch_to (int): Intermediate rectangle size param.
            Defaults to 4. Rectangle size is `stretch_to` * 2 + 1.
        duration (int): Animation duration in ms.
            Defaults to 250 ms.

    Returns:
        BaseAnimation: Point pulse animation.

    """
    return ParallelAnimation(
        [RectanglePositionAnimation(
            start=((p - stretch_from) * scale,
                   (p + 1 + stretch_from) * scale),
            finish=((p - stretch_to) * scale,
                    (p + 1 + stretch_to) * scale),
            color=img[p.y, p.x].tolist(),
            thickness=-1,
            duration=duration,
            easing=EasingFunc.OUT
        ), RectanglePositionAnimation(
            start=((p - stretch_from) * scale - border_thickness // 2,
                   (p + 1 + stretch_from) * scale + border_thickness // 2),
            finish=((p - stretch_to) * scale - border_thickness // 2,
                    (p + 1 + stretch_to) * scale + border_thickness // 2),
            color=(255, 255, 255),
            thickness=border_thickness,
            duration=duration,
            easing=EasingFunc.OUT
        )],
        fps=fps,
        repeat=RepeatMode.SWING
    )


def line_propagate(p1: Point2D, p2: Point2D, duration: int = None,
                   reverse: bool = False) -> BaseAnimation:
    """
    Line stretching from one point to another animation.

    Args:
        p1 (Point2D): First point.
        p2 (Point2D): Second point.
        duration (int): Animation duration in ms.
            Defaults to None. If set to None the distance between
            points is used as a duration.
        reverse (bool): Whether to reverse the animation.
            Defaults to False.

    Returns:
        BaseAnimation: Line propagate animation.

    """
    start = (p1 * scale + scale // 2, p1 * scale + scale // 2)
    finish = (p1 * scale + scale // 2, p2 * scale + scale // 2)
    if reverse:
        start, finish = finish, start
    return LinePositionAnimation(
        start=start,
        finish=finish,
        color=(0, 0, 0),
        thickness=line_thickness,
        duration=l2_metric(p1, p2) if duration is None else duration,
        fps=fps,
        repeat=RepeatMode.STICK
    )


def line_appear(p1: Point2D, p2: Point2D, duration: int = 250,
                reverse: bool = False) -> BaseAnimation:
    """
    Line appear animation.

    Args:
        p1 (Point2D): First point.
        p2 (Point2D): Second point.
        duration (int): Animation duration in ms.
            Defaults to 250 ms.
        reverse (bool): Whether to reverse the animation.
            Defaults to False.

    Returns:
        BaseAnimation: Line appear animation.

    """
    animation = LineThicknessAnimation(
        start=1,
        finish=line_thickness,
        position=(p1 * scale + scale // 2,
                  p2 * scale + scale // 2),
        color=(0, 0, 0),
        duration=duration,
        fps=fps,
        repeat=RepeatMode.STICK,
        easing=EasingFunc.OUT
    )
    if reverse:
        animation.repeat = RepeatMode.ONEOFF
        animation.reverse()
    return animation


def line_instant(p1: Point2D, p2: Point2D) -> BaseAnimation:
    """
    Instanteneous line animation.

    Args:
        p1 (Point2D): First point.
        p2 (Point2D): Second point.

    Returns:
        BaseAnimation: Line animation.

    """
    return LineAnimation(
        {"position": (p1 * scale + scale // 2,
                      p2 * scale + scale // 2),
         "color": (0, 0, 0),
         "thickness": line_thickness}, dict(),
        duration=0,
        step=1,
        repeat=RepeatMode.STICK
    )
