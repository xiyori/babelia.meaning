import numpy as np
from abc import ABC, abstractmethod

from .enums import State, RepeatMode


class BaseAnimation(ABC):
    """
    Abstract base class for all animations.

    Animation is viewed as a function of time:
        A: [0, +inf] -> F

    Function A is represented as a composition of three functions:
        A = D ∘ phi ∘ theta,

        theta: [0, +inf] -> [0, duration]
        phi: [0, duration] -> [0, 1] (*)
        D: [0, 1] -> F (**)
    where theta handles repeat modes, phi is used for manipulations
    with the animation speed (e.g. easing), D stands for `_draw` method,
    which generates frames based on phi value.

    Implementing abstract methods `_draw` and `_phi` allows creating
    nearly any desired animation. Then `advance` method can be used
    to display animation frame by frame.

        (*)  See details in `_phi` method docstring.
        (**) See details in `_draw` method docstring.

    Args:
        duration (int): Animation duration in milliseconds.
        step (int): Time interval between frames in milliseconds.
            Defaults to None.
        fps (int): Animation frame rate. Can be specified instead of `step`.
            Defaults to None.
        repeat (RepeatMode): Animation repeat mode.
            Defaults to RepeatMode.ONEOFF. See enum class for details.

    Raises:
        ValueError: If `step` and `fps` are set simultaneously.

    """

    def __init__(self, duration: int, step: int = None, fps: int = None,
                 repeat = RepeatMode.ONEOFF):
        if duration < 1:
            duration = 1
        self._duration = int(duration)
        if fps is not None:
            if step is not None:
                raise ValueError("cannot set step and fps at the same time")
            self.fps = fps
        else:
            self._step = step
        self._repeat = repeat

        # Default values
        self._state = State.READY
        self._start_time = None
        self._time = None
        self._reversed = False

    @abstractmethod
    def _draw(self, phi: float, img: np.ndarray):
        """
        Generate frame from phi value.
            D: [a, b] -> F
            a <= 0, b >= 1

        See class docstring for details.

        Args:
            phi (float): Phi value.
                0 corresponds to animation start.
                1 corresponds to animation finish.
            img (np.ndarray): Image to draw on.

        """
        pass

    @abstractmethod
    def _phi(self, dt: int) -> float:
        """
        Tweak the speed of animation.
            phi: [0, duration] -> [a, b]
            a <= 0, b >= 1

            phi(0) = 0
            phi(duration) = 1

        See class docstring for details.

        Args:
            dt (int): Time variable.
                0 corresponds to start time.
                duration corresponds to finish time.

        Returns:
            float: Phi value.
                0 corresponds to animation start.
                1 corresponds to animation finish.

        """
        pass

    def _theta(self, dt: int) -> int:
        """
        Process time according to repeat mode.
            theta: [0, +inf] -> [0, duration]

        See class docstring for details.

        Args:
            dt (int): Time since the animation start.
                0 corresponds to start time.

        Returns:
            int: Time variable.
                0 corresponds to start time.
                duration corresponds to finish time.

        """
        if self._reversed:
            dt = self._duration - dt

        if (self._repeat == RepeatMode.RETURN or
                self._repeat == RepeatMode.SWING) and dt > self.duration:
            dt = 0
        elif self._repeat == RepeatMode.STICK and dt < 0:
            dt = self._duration
        elif self._repeat == RepeatMode.REPEAT:
            dt = dt % self._duration
        elif self._repeat == RepeatMode.SWING:
            if dt < self._duration / 2:
                dt = dt * 2
            else:
                dt = (self._duration - dt) * 2
        elif self._repeat == RepeatMode.CYCLE:
            dt = dt % self._duration
            if dt < self._duration / 2:
                dt = dt * 2
            else:
                dt = (self._duration - dt) * 2
        return np.clip(dt, a_min=0, a_max=self._duration).item()

    def draw(self, dt: int, img: np.ndarray):
        """
        Full animation transform.
            A: [0, duration] -> F
            A = D ∘ phi ∘ theta

        See class docstring for details.

        Args:
            dt (int): Time since the animation start.
                0 corresponds to start time.
            img (np.ndarray): Image to draw on.

        """
        if self.disabled:
            return

        self._draw(self._phi(self._theta(dt)), img)  # Main function A(dt)

        if dt > self._duration:  # Handle repeat modes that change the state
            if self._repeat == RepeatMode.ONEOFF:
                self._state = State.DISABLED
            elif (self._repeat == RepeatMode.RETURN or
                  self._repeat == RepeatMode.STICK or
                  self._repeat == RepeatMode.SWING):
                self._state = State.FINISHED

    def pending_advance(self, time: int) -> bool:
        """
        Check if a new frame is ready to be displayed.

        Args:
            time (int): Absolute time.

        Returns:
            bool: True if a new frame is ready.

        """
        return (self._state == State.READY or
                (self._state == State.ACTIVE and time - self._time >= self._step))

    def advance(self, time: int, img: np.ndarray):
        """
        Update absolute time value and redraw animation.

        Args:
            time (int): Absolute time.
            img (np.ndarray): Image to draw on.

        """
        if self.disabled:
            return

        # Activate new animation
        if self._state == State.READY:
            self._state = State.ACTIVE
            self._start_time = time

        # Update absolute time
        self._time = self._start_time + (time - self._start_time) // self._step * self._step

        # Redraw animation
        self.draw(time - self._start_time, img)

    def reverse(self):
        """
        Reverse animation direction.

        """
        if self.disabled:
            return

        self._reversed = not self._reversed
        if self._state == State.ACTIVE:
            # Change start time to match the progress of active animation
            self._start_time = self._time * 2 - self._duration - self._start_time
        else:
            self._state = State.READY

    def reset(self):
        """
        Reset animation back to initial state.

        Results in animation restart.

        """
        if self.disabled:
            return

        self._reversed = False
        self._state = State.READY

    def skip(self):
        """
        Skip animation and display the final state if possible.

        Does nothing if no final state is defined.

        """
        if self.disabled:
            return

        # Change start time to skip animation
        if (self._repeat == RepeatMode.RETURN or
                self._repeat == RepeatMode.STICK or
                self._repeat == RepeatMode.SWING):
            self._start_time = self._time - (self._duration + 1)

    def disable(self):
        """
        Disable animation.

        """
        self._state = State.DISABLED

    @property
    def duration(self) -> int:
        """
        Animation duration in milliseconds.

        """
        return self._duration

    @property
    def step(self) -> int:
        """
        Time interval between frames in milliseconds.

        """
        return self._step

    @step.setter
    def step(self, value: int):
        self._step = value

    @property
    def fps(self) -> int:
        """
        Animation frame rate.

        """
        return 1000 // self._step

    @fps.setter
    def fps(self, value: int):
        self._step = 1000 // value

    @property
    def repeat(self) -> RepeatMode:
        """
        Animation repeat mode.

        See animation.enums.repeat_mode for details.

        """
        return self._repeat

    @repeat.setter
    def repeat(self, value: RepeatMode):
        self._repeat = value

    @property
    def disabled(self) -> bool:
        """
        True if animation is disabled.

        """
        return self._state == State.DISABLED
