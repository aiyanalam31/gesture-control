# tracking.py

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from config import MODEL_PATH


def create_detector():
    """
    Initializes and returns a MediaPipe HandLandmarker detector.

    Returns:
        vision.HandLandmarker instance
    """
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.8
    )
    return vision.HandLandmarker.create_from_options(options)


def detect_landmarks(detector, frame):
    """
    Runs hand landmark detection on a single BGR frame.

    Args:
        detector: HandLandmarker instance from create_detector()
        frame: BGR numpy array from OpenCV
    Returns:
        HandLandmarkerResult object
    """
    rgb = __import__('cv2').cvtColor(frame, __import__('cv2').COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    return detector.detect(mp_image)