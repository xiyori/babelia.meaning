from enum import Enum


class EasingFunc(Enum):
    """
    Easing function enum.

    Formulas and graphs can be found at https://www.desmos.com/calculator/m6ntd0rbnn

    """

    LINEAR   = 0  #: Linear function, no easing; phi: [0, duration] -> [0, 1]
    IN       = 1  #: Ease in;                    phi: [0, duration] -> [0, 1]
    OUT      = 2  #: Ease out;                   phi: [0, duration] -> [0, 1]
    SMOOTH   = 3  #: Ease both in and out;       phi: [0, duration] -> [0, 1]
    PULSEIN  = 4  #: Negative phi pulse in;      phi: [0, duration] -> [1 - s, 1]
    PULSEOUT = 5  #: Negative phi pulse out;     phi: [0, duration] -> [0, s]
