import numpy as np


def l1_norm(x, y):
    return np.abs(x) + np.abs(y)


def l2_norm(x, y):
    return (x ** 2 + y ** 2) ** (1 / 2)


def linf_norm(x, y):
    return np.maximum(np.abs(x), np.abs(y))
