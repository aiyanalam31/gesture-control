# main.py

import cv2
import pyautogui
import time

from config import CAMERA_INDEX, CLICK_COOLDOWN
from tracking import create_detector, detect_landmarks
from gesture import get_gesture, stable_gesture
from mouse import move_cursor, left_click, right_click, mouse_down, mouse_up


def main():
    detector = create_detector()
    cap = cv2.VideoCapture(CAMERA_INDEX)
    screen_w, screen_h = pyautogui.size()

    last_click_time = 0
    drag_active = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        result = detect_landmarks(detector, frame)
        gesture_label = "none"

        if result.hand_landmarks:
            lm = result.hand_landmarks[0]
            move_cursor(lm, screen_w, screen_h)

            raw_gesture = get_gesture(lm, screen_w, screen_h)
            confirmed = stable_gesture(raw_gesture)
            gesture_label = raw_gesture

            now = time.time()

            if confirmed == "pinch" and (now - last_click_time) > CLICK_COOLDOWN:
                left_click()
                last_click_time = now

            elif confirmed == "fist":
                if not drag_active:
                    mouse_down()
                    drag_active = True

            elif confirmed == "peace" and (now - last_click_time) > CLICK_COOLDOWN:
                right_click()
                last_click_time = now

            else:
                if drag_active:
                    mouse_up()
                    drag_active = False

        # HUD overlay
        cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
        cv2.putText(frame, f"Gesture: {gesture_label}", (10, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 180), 2)

        cv2.imshow("Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if drag_active:
        mouse_up()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()