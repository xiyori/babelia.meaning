from .point2d import Point2D


def segments_intersect(p1: Point2D, p2: Point2D,
                       q1: Point2D, q2: Point2D) -> bool:
    """
    Determine whether 2 line segments intersect internally.

    End point intersection doesn't count.

    Args:
        p1 (Point2D): First segment starting point.
        p2 (Point2D): First segment final point.
        q1 (Point2D): Second segment starting point.
        q2 (Point2D): Second segment final point.

    Returns:
        bool: True if line segments intersect.

    """
    p = p1
    r = p2 - p1
    q = q1
    s = q2 - q1
    if r @ s == 0 and (q - p) @ r == 0:    # Segments are collinear
        t_0 = (q - p) * r / (r * r)
        t_1 = t_0 + s * r / (r * r)
        if t_1 < t_0:
            t_0, t_1 = t_1, t_0
        if not (t_0 <= t_1 <= 0 or 1 <= t_0 <= t_1):
            return True
    elif r @ s == 0:                       # Segments are parallel
        pass
    elif (0 < (q - p) @ s / (r @ s) < 1 and
          0 < (q - p) @ r / (r @ s) < 1):  # Segments intersect
        return True
    return False
