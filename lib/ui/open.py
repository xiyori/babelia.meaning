import cv2
import numpy as np

from time import perf_counter_ns
from typing import Optional, Sequence

from . import animations as A
from lib.animation import AnimationManager, ParallelAnimation, SequenceAnimation, RepeatMode
from lib.utils import monitor_info, open_image, open_bookmark, print_exception, print_red
from lib.math_utils import Point2D, line2d, metrics, walk, select_color
from lib.enums import OpenMode, EditorState, MagnetState
from lib.command import Command, OpenParser, MetricParser, CoordsParser, IntersectParser, \
    SpeedParser, PointsParser, ScaleParser, TimeLimitParser

#: Time in ms to wait for the mouse to move before displaying a selection.
still_wait_time = 500
#: Time in ms to wait between the consecutive strokes in bookmark mode.
stroke_interval = 250
#: Distance in original image pixels for the magnet to activate.
magnet_dist = 12

imgname: str = None                #: Opened image filename without the file extension.
mode: OpenMode = None              #: Open mode.
metric: metrics.BaseMetric = None  #: Metric to use in the nearest point walk.
allow_intersections: bool = None   #: Allow line self-intersections in the nearest point walk.
time_limit: int = None             #: Time limit for the nearest point walk computation.
img: np.ndarray = None             #: Current original image.
img_show: np.ndarray = None        #: Scaled image.
scale: int = None                  #: Image scaling param.
manager: AnimationManager = None   #: OpenCV animation manager.
#: Current point, used to detect mouse movement and as the last point of the current stroke in draw mode.
current_point: Point2D = None
start_time: int = None             #: Starting time, used in waiting for the mouse to move.
state: EditorState = None          #: Editor state.
mstate: MagnetState = None         #: Magnet state.
vertices: list = None              #: Selected pixels coordinates in draw mode.
strokes: list = None               #: List of strokes. A stroke is a sequence of points.
undone_strokes: list = None        #: List of undone strokes. Cleared when a new stroke is added.

l2_metric = metrics.L2Metric()


def open(response: Command) -> Optional[tuple]:
    """
    Open command interface (editor).

    Args:
        response (Command): User command.

    Returns:
        :obj:`str`, optional: Opened image filename without
            the file extension.
        :obj:`list` of :obj:`list` of :obj:`Point2D`, optional: List of strokes.

    """
    global imgname, mode, metric, allow_intersections, time_limit, \
        img, img_show, scale, manager, current_point, start_time, \
        state, mstate, vertices, strokes, undone_strokes

    # Parse command options
    try:
        (mode, metric, current_point, allow_intersections, speed,
         disable_points, scale, time_limit), args, toggled = response.parse_options(
            parsers=[OpenParser(), MetricParser(), CoordsParser(), IntersectParser(),
                     SpeedParser(), PointsParser(), ScaleParser(), TimeLimitParser()],
            return_toggled=True
        )
        filename = args[0]
        open_mode_toggled = toggled[0]
    except ValueError as e:
        print_exception(e)
        return None
    except IndexError:
        print_red("Filename missing!")
        return None

    # Try to load bookmark if open mode is BOOKMARK or not set
    if not open_mode_toggled or mode == OpenMode.BOOKMARK:
        try:
            filename, strokes = open_bookmark(filename)
            mode = OpenMode.BOOKMARK
        except FileNotFoundError as e:
            if mode == OpenMode.BOOKMARK:
                print_exception(e)
                return None
        except BaseException as e:
            print_red(f"Bookmark \"{filename}\" corrupted:")
            print_exception(e)
            return None
    else:
        strokes = []

    # Load image
    try:
        imgname, img = open_image(filename)
    except FileNotFoundError as e:
        print_exception(e)
        return None

    # Cosine similarity metric requires center point coordinates
    if metric.name == "cos":
        metric.p_center = Point2D(img.shape[1], img.shape[0]) // 2

    # Scale UI according to monitor resolution
    max_scale = max(1, min(monitor_info.work_h // img.shape[0],
                           monitor_info.work_w // img.shape[1]))
    if scale is None:
        scale = max_scale
    else:
        scale = min(scale, max_scale)
    A.scale = scale
    A.line_thickness = scale + scale // 5
    A.border_thickness = scale - scale * 3 // 5
    A.img = img

    # Scaled image
    img_show = cv2.resize(img, dsize=(img.shape[1] * scale,
                                      img.shape[0] * scale),
                          interpolation=cv2.INTER_NEAREST)

    # OpenCV animation manager
    manager = AnimationManager(imgname, img_show)

    # Default values
    start_time = None
    state = EditorState.INIT

    # Manual coords option
    if current_point is None:
        current_point = Point2D(-1, -1)
    elif mode == OpenMode.FAST:
        select_fast()
        state = EditorState.LOCK
    elif mode != OpenMode.BOOKMARK:
        select_normal()
        state = EditorState.LOCK
        if mode == OpenMode.DRAW:
            state = EditorState.DRAW_STANDBY
            points_pulse(vertices)

    # Bookmark animation
    if mode == OpenMode.BOOKMARK:
        try:
            lines = []
            points = []
            line_timestamps = [0]
            point_timestamps = [0]
            for path in strokes:
                for i in range(1, len(path)):
                    duration = l2_metric(path[i - 1], path[i]) / speed
                    lines.append(A.line_propagate(path[i - 1], path[i], duration))
                    points.append(A.point_appear(path[i - 1]))
                    line_timestamps.append(line_timestamps[-1] + duration)
                    point_timestamps.append(point_timestamps[-1] + duration)
                points.append(A.point_appear(path[-1]))
                line_timestamps[-1] = line_timestamps[-1] + stroke_interval / max(speed, 1)
                point_timestamps.append(line_timestamps[-1])
            manager["lines"] = SequenceAnimation(
                lines,
                line_timestamps,
                fps=A.fps,
                repeat=RepeatMode.STICK
            )
            if not disable_points:
                manager["points"] = SequenceAnimation(
                    points,
                    point_timestamps,
                    fps=A.fps,
                    repeat=RepeatMode.STICK
                )
                manager.set_zindex("points", 1)
        except BaseException as e:
            print_red(f"Bookmark corrupted:")
            print_exception(e)
            return None

    cv2.imshow(imgname, img_show)                  # Display image in an OpenCV window
    cv2.setMouseCallback(imgname, mouse_callback)  # Set up mouse event handler

    # Main editor loop
    while cv2.getWindowProperty(imgname, cv2.WND_PROP_VISIBLE) > 0:
        key = cv2.waitKey(1) & 0xFF                 # Wait for a keypress

        if key == 27:                               # Break when 'Esc' is pressed
            break
        elif mode == OpenMode.DRAW and key == 122:  # Undo when 'Z' is pressed
            if len(strokes) > 0:
                path = strokes.pop()
                undone_strokes.append(path)
                for i in range(1, len(path)):
                    manager[f"line_{path[i - 1]}_{path[i]}"] = A.line_appear(path[i - 1],
                                                                             path[i],
                                                                             reverse=True)
                    manager[f"point_{path[i - 1]}"].reset()
                manager[f"point_{path[-1]}"].reset()
        elif mode == OpenMode.DRAW and key == 121:  # Redo when 'Y' is pressed
            if len(undone_strokes) > 0:
                path = undone_strokes.pop()
                strokes.append(path)
                for i in range(1, len(path)):
                    manager[f"line_{path[i - 1]}_{path[i]}"] = A.line_appear(path[i - 1],
                                                                             path[i])
                    manager[f"point_{path[i - 1]}"].reset()
                manager[f"point_{path[-1]}"].reset()
        elif mode == OpenMode.DRAW and key == 100:  # Deselect when 'D' is pressed
            state = EditorState.INIT
            manager.clear()
            for path in strokes:
                for i in range(1, len(path)):
                    manager[f"lineth_{path[i - 1]}_{path[i]}"] = A.line_appear(path[i - 1],
                                                                               path[i],
                                                                               reverse=True)
            points_disappear(vertices)

        # Show selection if the mouse pointer has not moved for `still_wait_time` ms
        if (state == EditorState.AWAIT and
                perf_counter_ns() // 1000000 - start_time >= still_wait_time):
            select_normal()

        manager.refresh()    # Redraw animations if needed

    cv2.destroyAllWindows()  # Close the OpenCV window

    # Return the results of editing if any
    return (imgname, strokes) if len(strokes) > 0 else None


def mouse_callback(event: int, x: int, y: int,
                   flags, param):
    """
    Mouse event handler.

    Args:
        event (int): OpenCV mouse event id.
        x (int): Mouse x coordinate.
        y (int): Mouse y coordinate.

    """
    global mode, manager, current_point, start_time, state, mstate, strokes, undone_strokes

    if mode != OpenMode.BOOKMARK and event == cv2.EVENT_MOUSEMOVE:  # Mouse move
        mouse_point = Point2D(x, y) // scale
        if state == EditorState.DRAW_DRAG:     # Line drawing in draw mode
            if mstate == MagnetState.STANDBY:  # Activate magnet
                if len(strokes[-1]) > 1:
                    dist = l2_metric(current_point, mouse_point)
                    semiplane = line2d.normal(strokes[-1][-2], current_point)(mouse_point)
                    if dist <= magnet_dist and semiplane < 0:
                        mstate = MagnetState.REMOVE
                if mstate == MagnetState.STANDBY:  # Add a new point to the current stroke
                    for p in vertices:
                        if p == current_point:
                            continue
                        dist = l2_metric(p, mouse_point)
                        semiplane = line2d.normal(current_point, p)(mouse_point)
                        if (dist <= magnet_dist and semiplane < 0 and
                                not line_exists(p, current_point)):
                            strokes[-1].append(p)
                            manager[f"line_{current_point}_{p}"] = A.line_instant(current_point, p)
                            manager[f"point_{p}"].reset()
                            current_point = p
                            break
            elif mstate == MagnetState.REMOVE:     # Remove the last point from the current stroke
                dist = l2_metric(current_point, mouse_point)
                semiplane = line2d.normal(strokes[-1][-2], current_point)(mouse_point)
                if dist > magnet_dist:
                    mstate = MagnetState.STANDBY
                elif semiplane > 0:
                    mstate = MagnetState.STANDBY
                    strokes[-1].pop()
                    manager[f"line_{strokes[-1][-1]}_{current_point}"].disable()
                    manager[f"point_{current_point}"].reset()
                    current_point = strokes[-1][-1]
            manager["drag_line"] = A.line_instant(current_point, mouse_point)
        elif (state == EditorState.INIT or state == EditorState.AWAIT or
              state == EditorState.SELECT) and mouse_point != current_point:
            if mode == OpenMode.NORMAL or mode == OpenMode.DRAW:  # Hide current selection and wait
                if state == EditorState.SELECT:
                    reverse_animations()
                current_point = mouse_point
                start_time = perf_counter_ns() // 1000000
                state = EditorState.AWAIT
            elif mode == OpenMode.FAST:  # Hide current selection and display a new one
                current_point = mouse_point
                select_fast()
    elif event == cv2.EVENT_LBUTTONUP:  # Mouse left button up
        if mode == OpenMode.DRAW:
            if state == EditorState.SELECT:       # Lock selection for drawing
                state = EditorState.DRAW_STANDBY
                strokes = []
                undone_strokes = []
                points_pulse(vertices)
            elif state == EditorState.DRAW_DRAG:  # Complete current stroke
                state = EditorState.DRAW_STANDBY
                if len(strokes[-1]) <= 1:
                    strokes.pop()
                else:
                    undone_strokes = []
                mouse_point = Point2D(x, y) // scale
                manager["drag_line"] = A.line_propagate(current_point,
                                                        mouse_point,
                                                        reverse=True)
        elif mode == OpenMode.BOOKMARK:  # Edit bookmark content
            mode = OpenMode.DRAW
            current_point = strokes[0][0]
            manager.clear()
            select_normal()
            state = EditorState.DRAW_STANDBY
            for path in strokes:
                for i in range(1, len(path)):
                    manager[f"line_{path[i - 1]}_{path[i]}"] = A.line_instant(path[i - 1], path[i])
            points_pulse(vertices)
        elif state == EditorState.LOCK:  # Unlock selection
            if mode == OpenMode.NORMAL:
                points_appear(strokes[0])
                reverse_animations()
            elif mode == OpenMode.FAST:
                manager.clear()
            strokes = []
            state = EditorState.INIT
        elif mode == OpenMode.NORMAL:    # Lock selection in normal mode
            if state == EditorState.SELECT:
                state = EditorState.LOCK
                points_pulse(strokes[0])
            else:
                select_normal()
                state = EditorState.LOCK
        elif mode == OpenMode.FAST:      # Lock selection in fast mode
            state = EditorState.LOCK
    elif (state == EditorState.DRAW_STANDBY and
          event == cv2.EVENT_LBUTTONDOWN):  # Mouse left button down, start a new stroke in draw mode
        mouse_point = Point2D(x, y) // scale
        current_point = vertices[np.argmin([l2_metric(p, mouse_point) for p in vertices])]
        strokes.append([current_point])
        manager["drag_line"] = A.line_instant(current_point, mouse_point)
        manager[f"point_{current_point}"].reset()
        mstate = MagnetState.STANDBY
        state = EditorState.DRAW_DRAG


def select_fast():
    """
    Show selection without animations.

    """
    global manager, strokes

    try:
        path = walk(img, current_point, metric, allow_intersections, time_limit)
    except (TimeoutError, IndexError) as e:
        print_exception(e)
        return
    strokes = [path]
    lines = []
    for i in range(1, len(path)):
        lines.append(A.line_instant(path[i - 1], path[i]))
    manager["path"] = ParallelAnimation(
        lines,
        step=1,
        repeat=RepeatMode.STICK
    )


def line_exists(p1: Point2D, p2: Point2D) -> bool:
    """
    Determine whether a line segment already exists.

    Args:
        p1 (Point2D): First point.
        p2 (Point2D): Second point.

    Returns:
        bool: True if a line segment exists.

    """
    for path in strokes:
        for i in range(1, len(path)):
            if ((path[i - 1] == p1 and path[i] == p2) or
                    (path[i - 1] == p2 and path[i] == p1)):
                return True
    return False


def select_normal():
    """
    Show selection with animations.

    """
    global manager, state, mstate, vertices, strokes, undone_strokes

    state = EditorState.SELECT
    if mode == OpenMode.NORMAL:
        try:
            path = walk(img, current_point, metric, allow_intersections, time_limit)
        except (TimeoutError, IndexError) as e:
            state = EditorState.INIT
            print_exception(e)
            return
        strokes = [path]
        for i in range(1, len(path)):
            manager[f"lineth_{path[i - 1]}_{path[i]}"] = A.line_appear(path[i - 1], path[i])
        points_appear(path)
    elif mode == OpenMode.DRAW:
        mstate = MagnetState.STANDBY
        undone_strokes = []
        vertices = list(select_color(img, img[current_point.y, current_point.x]))
        points_appear(vertices)


def reverse_animations():
    """
    Reverse point and line appear animations.

    """
    global manager

    for key, animation in manager.items():
        if key.startswith("point") or key.startswith("lineth"):
            animation.repeat = RepeatMode.ONEOFF
            animation.reverse()
        else:
            animation.disable()


def points_appear(points: Sequence[Point2D]):
    """
    Enlarge selected pixels.

    Args:
        points (:obj:`Sequence` of :obj:`Point2D`):
            Selected pixels coordinates.

    """
    global manager

    for p in points:
        manager[f"point_{p}"] = A.point_appear(p)
        manager.set_zindex(f"point_{p}", 1)


def points_disappear(points: Sequence[Point2D]):
    """
    Contract enlarged pixels.

    Args:
        points (:obj:`Sequence` of :obj:`Point2D`):
            Selected pixels coordinates.

    """
    global manager

    for p in points:
        manager[f"point_{p}"] = A.point_appear(p, reverse=True)
        manager.set_zindex(f"point_{p}", 1)


def points_pulse(points: Sequence[Point2D]):
    """
    Enlarged pixels pulse.

    Args:
        points (:obj:`Sequence` of :obj:`Point2D`):
            Selected pixels coordinates.

    """
    global manager

    for p in points:
        manager[f"point_{p}"] = A.point_pulse(p)
        manager.set_zindex(f"point_{p}", 1)
