# Gesture Control

Control your computer with hand gestures using your webcam — no hardware required.

![demo](assets/demo.gif)

## Gestures
| Gesture | Action |
|---------|--------|
| ☝️ Point | Move cursor |
| 🤏 Pinch | Left click |
| ✌️ Peace | Right click |
| ✊ Fist | Click & drag |

## Setup
1. Download `hand_landmarker.task` from [MediaPipe](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task) and place it in the project root
2. Install dependencies:
   pip install -r requirements.txt
3. Run:
   python main.py

## How it works
- MediaPipe detects 21 hand landmarks per frame
- Landmark positions are classified into gestures using finger extension logic
- A gesture buffer requires 5 consecutive matching frames before firing
- Cursor position is smoothed with an exponential moving average
```