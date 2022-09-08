import os
import cv2
import numpy as np

from typing import Optional, Sequence

from .open_image import open_image
from lib.math_utils import Point2D


MAX_IMAGE_SIZE = 20000

export_dir = "data/export/"


def exported_image_exists(filename: str) -> bool:
    """
    Check if an exported image already exists on disk.

    Args:
        filename (str): Export image name.

    Returns:
        bool: True if an image exists.

    """
    return os.path.isfile(export_dir + filename + ".png")


def export_image(filename: str, imgname: str,
                 strokes: Sequence[Sequence[Point2D]],
                 scale: int = 5,
                 color: tuple = (0, 0, 0),
                 thickness: Optional[int] = None,
                 transparent: bool = False,
                 line_type: int = cv2.LINE_AA):
    """
    Save bookmark to disk.

    Args:
        filename (str): Export image name.
        imgname (str): Background image name.
        strokes (:obj:`Sequence` of :obj:`Sequence` of :obj:`Point2D`):
            List of strokes to export.
        scale (int): Image scaling param. Defaults to 5.
        color (tuple): Line color in BGR format. Defaults to black.
        thickness (int): Line thickness. Defaults to None.
            If set to None thickness is set automatically.
        transparent (bool): Whether to use transparent background.
            Background image is still used to determine image size.
            Defaults to False.
        line_type (int): OpenCV line renderer. Defaults to cv2.LINE_AA.

    """
    _, img = open_image(imgname)
    if transparent:
        img.fill(0)

    max_scale = max(1, min(MAX_IMAGE_SIZE // img.shape[0],
                           MAX_IMAGE_SIZE // img.shape[1]))
    scale = min(scale, max_scale)
    if thickness is None:
        thickness = scale + scale // 5

    # Scaled image
    img_export = cv2.resize(img, dsize=(img.shape[1] * scale,
                                        img.shape[0] * scale),
                            interpolation=cv2.INTER_NEAREST)

    for path in strokes:
        for i in range(1, len(path)):
            cv2.line(img_export,
                     (path[i - 1] * scale + scale // 2).tuple,
                     (path[i] * scale + scale // 2).tuple,
                     color=(255, 255, 255) if transparent else color,
                     thickness=thickness, lineType=line_type)

    if transparent:
        alpha = img_export[:, :, :1].copy()
        for channel, c in zip(np.moveaxis(img_export, 2, 0), color):
            channel.fill(c)
        img_export = np.concatenate((img_export, alpha), axis=2)

    if not os.path.isdir(export_dir):
        os.mkdir(export_dir)
    cv2.imwrite(export_dir + filename + ".png", img_export)
