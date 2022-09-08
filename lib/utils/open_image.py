import os
import cv2
import numpy as np

from .round_image import round_image


images_dir = "data/"
converted_dir = "data/__converted__/"
_images = None


def get_images(reload: bool = False) -> list:
    """
    Get images library.

    Args:
        reload (bool): Whether to reload library from disk.
            Defaults to False.

    Returns:
        list: Images library.

    """
    global _images
    if reload or _images is None:
        if not os.path.isdir(images_dir):
            os.mkdir(images_dir)
        _images = [name for name in os.listdir(images_dir) if
                   name.lower().endswith(".png") or
                   name.lower().endswith(".jpg") or
                   name.lower().endswith(".jpeg") or
                   name.lower().endswith(".gif") or
                   name.lower().endswith(".bmp")]
        _images.sort()
    return _images


def split_extension(filename: str) -> tuple:
    """
    Split filename into base name and file extension.

    Args:
        filename (str): Filename to be split.

    Returns:
        str: Base name.
        str: File extension.

    """
    split_pos = len(filename) - filename[::-1].index(".") - 1
    return filename[:split_pos], filename[split_pos:]


def open_image(filename: str) -> tuple:
    """
    Load image from disk and convert if needed.

    Args:
        filename (str): Image name or index.

    Returns:
        str: Image name.
        np.ndarray: OpenCV image (BGR).

    """
    images = get_images()

    try:
        file_id = int(filename)
        imgname = images[file_id]
    except (ValueError, IndexError):
        imgname = filename

    try:
        base, ext = split_extension(imgname)
    except ValueError:
        base, ext = imgname, ""

    # If a converted version already exists
    converted_path = converted_dir + base + ".png"
    if os.path.isfile(converted_path):
        return base, cv2.imread(converted_path)

    # Search for a base name in the library
    img_path = images_dir + imgname
    if not os.path.isfile(img_path):
        for name in images:
            base, ext = split_extension(name)
            if base == imgname:
                img_path += ext
                break
        else:
            raise FileNotFoundError(f"image \"{imgname}\" not found")

    # Convert image to 4096 babelia color format
    print("Opening file for the first time, please wait...")
    img = round_image(cv2.imread(img_path))
    cv2.imwrite(converted_path, img)
    return base, img
