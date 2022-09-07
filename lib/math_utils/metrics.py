from abc import ABC, abstractmethod

from . import norms, Point2D


class BaseMetric(ABC):
    """
    Base 2D metric class.

    Args:
        name (str): Metric name.
        mode (str): {"min", "max"}
            Metric mode:
            "min": Lower values indicate closer points;
            "max": Higher values indicate closer points.

    Raises:
        ValueError: If `mode` value is not valid.

    """

    def __init__(self, name: str, mode: str):
        self.name = name
        if mode == "min":
            self.compare = lambda a, b: a < b
            self.key = lambda x: x
        elif mode == "max":
            self.compare = lambda a, b: a > b
            self.key = lambda x: -x
        else:
            raise ValueError(f"mode \"{mode}\" is not supported")
        self.mode = mode

    @abstractmethod
    def __call__(self, p1: Point2D, p2: Point2D) -> float:
        """
        Measure the metric between 2 points.

        Args:
            p1 (Point2D): First point.
            p2 (Point2D): Second point.

        Returns:
            float: Metric value.

        """
        pass


class NormInducedMetric(BaseMetric):
    def __init__(self, name: str, norm):
        super(NormInducedMetric, self).__init__(name, mode="min")
        self.norm = norm

    def __call__(self, p1: Point2D, p2: Point2D) -> float:
        return (p1 - p2).norm(self.norm)


class L1Metric(NormInducedMetric):
    def __init__(self):
        super(L1Metric, self).__init__(name="l1",
                                       norm=norms.l1_norm)


class L2Metric(NormInducedMetric):
    def __init__(self):
        super(L2Metric, self).__init__(name="l2",
                                       norm=norms.l2_norm)


class LInfMetric(NormInducedMetric):
    def __init__(self):
        super(LInfMetric, self).__init__(name="linf",
                                         norm=norms.linf_norm)


class CosMetric(BaseMetric):
    def __init__(self, p_center: Point2D = None):
        super(CosMetric, self).__init__(name="cos", mode="max")
        self.p_center = p_center

    def __call__(self, p1: Point2D, p2: Point2D) -> float:
        p1 = p1 - self.p_center
        p2 = p2 - self.p_center
        return p1 * p2 / (p1.norm() * p2.norm())
