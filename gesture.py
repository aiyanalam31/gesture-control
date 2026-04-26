# gesture.py

import numpy as np
from config import BUFFER_SIZE, PINCH_RATIO

gesture_buffer = []


def finger_up(lm, tip, pip):
    """Returns True if a finger is extended (tip above pip joint)."""
    return lm[tip].y < lm[pip].y


def get_gesture(lm, screen_w, screen_h):
    """
    Classify hand pose from MediaPipe landmarks.

    Args:
        lm: List of 21 NormalizedLandmark objects
        screen_w: Screen width in pixels
        screen_h: Screen height in pixels
    Returns:
        One of: 'pinch', 'peace', 'point', 'fist', 'open'
    """
    hand_size = np.hypot(
        (lm[0].x - lm[12].x) * screen_w,
        (lm[0].y - lm[12].y) * screen_h
    )

    thumb_up  = lm[4].x < lm[3].x
    index_up  = finger_up(lm, 8, 6)
    middle_up = finger_up(lm, 12, 10)
    ring_up   = finger_up(lm, 16, 14)
    pinky_up  = finger_up(lm, 20, 18)

    pinch_dist = np.hypot(
        (lm[4].x - lm[8].x) * screen_w,
        (lm[4].y - lm[8].y) * screen_h
    )
    pinching = pinch_dist < (hand_size * PINCH_RATIO)

    if pinching and index_up:
        return "pinch"
    elif index_up and middle_up and not ring_up and not pinky_up:
        return "peace"
    elif index_up and not middle_up and not ring_up and not pinky_up:
        return "point"
    elif not index_up and not middle_up and not ring_up and not pinky_up and not thumb_up:
        return "fist"
    else:
        return "open"


def stable_gesture(gesture):
    """
    Returns a gesture only once it has been held for BUFFER_SIZE consecutive frames.

    Args:
        gesture: Raw gesture string from get_gesture()
    Returns:
        Confirmed gesture string, or None if not yet stable
    """
    gesture_buffer.append(gesture)
    if len(gesture_buffer) > BUFFER_SIZE:
        gesture_buffer.pop(0)
    if gesture_buffer.count(gesture) == BUFFER_SIZE:
        return gesture
    return None