from enum import Enum


class EditorState(Enum):
    """
    Editor state enum.

    """

    INIT         = 0  #: Initial editor state.
    AWAIT        = 1  #: Waiting for the mouse pointer to stop moving for `still_wait_time` ms.
    SELECT       = 2  #: Selection is visible, erased on mouse move.
    LOCK         = 3  #: Selection is locked, unaffected by mouse move. Unlocked on mouse click.
    DRAW_STANDBY = 4  #: Selection is locked in DRAW open mode, erased on 'D' press.
    DRAW_DRAG    = 5  #: A line is being drawn, completed on mouse button release.
