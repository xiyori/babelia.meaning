import numpy as np

from time import perf_counter_ns
from typing import Iterator

from . import metrics
from .point2d import Point2D
from .segments_intersect import segments_intersect


def walk(img: np.ndarray, p_start: Point2D,
         metric: metrics.BaseMetric = metrics.L2Metric(),
         allow_intersections: bool = False,
         time_limit: int = 500) -> list:
    """
    Perform nearest point walk using image pixels of the same color.

    Args:
        img (np.ndarray): OpenCV image to select pixels from.
        p_start (Point2D): Starting point for the walk.
        metric (metrics.BaseMetric): Metric to measure the distance
            between points. Defaults to metrics.L2Metric.
        allow_intersections (bool): Whether to allow line
            self-intersections. Defaults to False.
        time_limit (int): Time limit for the computations in ms.
            Defaults to 500 ms.

    Returns:
        :obj:`list` of :obj:`Point2D`: A sequence of points visited
            in the walk.

    """
    start_time = perf_counter_ns() // 1000000
    color = img[p_start.y, p_start.x]

    visited = [p_start]
    remaining = set(select_color(img, color))
    remaining.remove(p_start)

    while len(remaining) > 0:
        if perf_counter_ns() // 1000000 - start_time > time_limit:
            raise TimeoutError(f"time limit of {time_limit} ms exceeded")

        p_current = visited[-1]
        dists = [(p, metric(p_current, p)) for p in remaining]

        if allow_intersections:
            p_closest = min(dists, key=lambda x: metric.key(x[1]))[0]
        else:
            dists.sort(key=lambda x: metric.key(x[1]))

            for p, dist in dists:
                for i in range(1, len(visited)):
                    if segments_intersect(visited[i - 1], visited[i],
                                          p_current, p):
                        break
                else:
                    p_closest = p
                    break
            else:
                break

        remaining.remove(p_closest)
        visited.append(p_closest)

    return visited


def select_color(img: np.ndarray, color: np.ndarray) -> Iterator[Point2D]:
    """
    Get coordinates of pixels with the same color.

    Args:
        img (np.ndarray): OpenCV image.
        color (np.ndarray): Color to select.

    Returns:
        (:obj:`Iterator` of :obj:`Point2D`): Coordinates iterator.

    """
    return map(Point2D, zip(*np.nonzero(np.all(img == color, axis=2))[::-1]))
