import cv2
import numpy as np
from tqdm import tqdm

NUM_CHANNEL_COLORS = 16               #: Number of colors per channel
NUM_COLORS = NUM_CHANNEL_COLORS ** 3  #: Total number of colors


def round_image(img: np.ndarray) -> np.ndarray:
    """
    Convert image to 4096 babelia color format.

    Args:
        img (np.ndarray): OpenCV image (BGR).

    Returns:
        np.ndarray: Converted image (BGR).

    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(int)
    for y in tqdm(range(img.shape[0]),
                  desc="Converting"):
        for x in range(img.shape[1]):
            dsts = ((img[y, x] - palette) ** 2).sum(axis=1)
            img[y, x] = palette[np.argmin(dsts)]
    return cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2BGR)


def number_to_color(number: np.ndarray) -> np.ndarray:
    """
    Convert color index in palette to RGB color.

    Args:
        number (np.ndarray): Color indices.

    Returns:
        np.ndarray: Array of RGB colors.

    """
    b = number % NUM_CHANNEL_COLORS
    number = number // NUM_CHANNEL_COLORS
    g = number % NUM_CHANNEL_COLORS
    r = number // NUM_CHANNEL_COLORS

    colors = np.stack((r, g, b), axis=1)
    return colors * 255 // (NUM_CHANNEL_COLORS - 1)


palette = number_to_color(np.arange(0, NUM_COLORS, dtype=int))
