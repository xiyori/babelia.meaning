import ctypes
from screeninfo import get_monitors


# Source: https://stackoverflow.com/a/44422362
try:
    # Query DPI Awareness (Windows 10 and 8)
    awareness = ctypes.c_int()
    errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))

    # Set DPI Awareness  (Windows 10 and 8)
    errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # the argument is the awareness level, which can be 0, 1 or 2:
    # for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 1)
except BaseException:
    pass

monitor_info = get_monitors()[0]
screen_w, screen_h = monitor_info.width, monitor_info.height
work_w = screen_w - 4   #: Approximate working area width.
work_h = screen_h - 60  #: Approximate working area height.
