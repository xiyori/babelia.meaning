from .point2d import Point2D


class Line2D:
    """
    Geometric 2D line.

    Args:
        a (float): Coefficient of x.
        b (float): Coefficient of y.
        c (float): Constant term.

    """

    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def __call__(self, p: Point2D) -> float:
        """
        Evaluate line expression at a point.

        Args:
            p (Point2D): Point to evaluate.

        Returns:
            float: Evaluation result.

        """
        return self.a * p.x + self.b * p.y + self.c


def from_2p(p1: Point2D, p2: Point2D) -> Line2D:
    """
    Construct 2D line from 2 points.

    Args:
        p1 (Point2D): First point.
        p2 (Point2D): Second point.

    Returns:
        Line2D: Constructed line.

    """
    return Line2D(p2.y - p1.y,
                  p1.x - p2.x,
                  p1.y * p2.x - p2.y * p1.x)


def normal(p1: Point2D, p2: Point2D) -> Line2D:
    """
    Construct a perpendicular to a segment between 2 points.

    The constructed perpendicular contains `p2`.

    Args:
        p1 (Point2D): First point.
        p2 (Point2D): Second point.

    Returns:
        Line2D: Constructed line.

    """
    a = p2.y - p1.y
    b = p1.x - p2.x
    c = a * p2.y - b * p2.x
    return Line2D(b, -a, c)
