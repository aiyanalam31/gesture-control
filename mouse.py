# mouse.py

import pyautogui
import numpy as np
from config import SMOOTHING_ALPHA, INPUT_ZONE

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

_smooth_x = 0.0
_smooth_y = 0.0


def move_cursor(lm, screen_w, screen_h):
    """
    Moves the cursor to the smoothed position of the index fingertip.

    Args:
        lm: List of 21 NormalizedLandmark objects
        screen_w: Screen width in pixels
        screen_h: Screen height in pixels
    """
    global _smooth_x, _smooth_y

    ix, iy = lm[8].x, lm[8].y
    zone_min, zone_max = INPUT_ZONE

    target_x = np.interp(ix, [zone_min, zone_max], [0, screen_w])
    target_y = np.interp(iy, [zone_min, zone_max], [0, screen_h])

    _smooth_x = SMOOTHING_ALPHA * target_x + (1 - SMOOTHING_ALPHA) * _smooth_x
    _smooth_y = SMOOTHING_ALPHA * target_y + (1 - SMOOTHING_ALPHA) * _smooth_y

    pyautogui.moveTo(_smooth_x, _smooth_y, duration=0)


def left_click():
    """Fires a left mouse click."""
    pyautogui.click()


def right_click():
    """Fires a right mouse click."""
    pyautogui.rightClick()


def mouse_down():
    """Presses and holds the left mouse button."""
    pyautogui.mouseDown()


def mouse_up():
    """Releases the left mouse button."""
    pyautogui.mouseUp()