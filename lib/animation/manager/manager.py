import cv2
import numpy as np
from time import perf_counter_ns
from collections import defaultdict


class AnimationManager(dict):
    """
    Manage animations inside OpenCV window.

    Args:
        window (str): OpenCV window name.
        img (np.ndarray): Background image.

    """

    def __init__(self, window: str, img: np.ndarray):
        super(AnimationManager, self).__init__()
        self._window = window
        self._img = img

        # Bidirectional dict for zindex management
        self._key2zindex = dict()
        self._zindex2key = defaultdict(set)

    def __setitem__(self, key: str, animation):
        """
        Add or set animation with a given id. Z-index is set to 0.

        Args:
            key (str): Animation name used in manager.
            animation (animation.BaseAnimation): Animation object.

        """
        self.set_zindex(key, 0)
        super(AnimationManager, self).__setitem__(key, animation)

    def _clean(self) -> bool:
        """
        Remove disabled animations.

        Returns:
            bool: If any animations were removed.

        """
        keys_to_remove = [key for key, animation in self.items()
                          if animation.disabled]
        for key in keys_to_remove:
            del self[key]

            # Bidirectional remove
            self._zindex2key[self._key2zindex[key]].remove(key)
            del self._key2zindex[key]
        return len(keys_to_remove) > 0

    def refresh(self):
        """
        Redraw animations if needed.

        Common usage is to refresh continuously in a loop.

        """
        time = perf_counter_ns() // 1000000

        # Redraw needed if some animations were removed
        if not self._clean():
            for animation in self.values():
                # Redraw needed if some animations can be advanced
                if animation.pending_advance(time):
                    break
            else:
                return

        # Redraw animations in z-order
        img_show = self._img.copy()
        for zindex in sorted(self._zindex2key.keys()):
            for key in self._zindex2key[zindex]:
                self[key].advance(time, img_show)

        # Display new image in the OpenCV window
        cv2.imshow(self._window, img_show)

    def clear(self):
        """
        Disable all animations.

        Animations will be removed from manager during the next refresh.

        """
        for animation in self.values():
            animation.disable()

    def get_zindex(self, key: str) -> int:
        """
        Get z-index of an animation.

        Args:
            key (str): Animation name.

        Returns:
            int: Animation z-index.

        """
        return self._key2zindex[key]

    def set_zindex(self, key: str, zindex: int):
        """
        Set z-index of an animation.

        Args:
            key (str): Animation name.
            zindex (int): Animation z-index.

        """
        # Bidirectional set
        if key in self._key2zindex:
            self._zindex2key[self._key2zindex[key]].remove(key)
        self._key2zindex[key] = zindex
        self._zindex2key[zindex].add(key)
