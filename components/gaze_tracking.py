from gaze_tracking import GazeTracking
import cv2
import pandas as pd


def track_gaze(video_path):
    gaze = GazeTracking()
    cap = cv2.VideoCapture(video_path)
    data = []
    frame_num = 0
    fps = cap.get(cv2.CAP_PROP_FPS)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gaze.refresh(frame)
        timestamp = frame_num / fps

        if gaze.is_blinking():
            direction = "blinking"
        elif gaze.is_right():
            direction = "right"
        elif gaze.is_left():
            direction = "left"
        elif gaze.is_center():
            direction = "center"
        else:
            direction = "unknown"

        data.append({"frame": frame_num, "time": timestamp, "direction": direction})
        frame_num += 1

    cap.release()
    df = pd.DataFrame(data)
    df.to_csv("data/gaze_data.csv", index=False)
