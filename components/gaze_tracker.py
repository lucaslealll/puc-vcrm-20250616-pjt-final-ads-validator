import av
from .gaze_tracking import GazeTracking
import cv2
import pandas as pd

GAZE = GazeTracking()


def track_gaze(video_path):
    cap = cv2.VideoCapture(video_path)
    data = []
    frame_num = 0
    fps = cap.get(cv2.CAP_PROP_FPS)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        GAZE.refresh(frame)
        timestamp = frame_num / fps

        if GAZE.is_blinking():
            direction = "blinking"
        elif GAZE.is_right():
            direction = "right"
        elif GAZE.is_left():
            direction = "left"
        elif GAZE.is_center():
            direction = "center"
        else:
            direction = "unknown"

        data.append({"frame": frame_num, "time": timestamp, "direction": direction})
        frame_num += 1

    cap.release()
    df = pd.DataFrame(data)
    df.to_csv("data/gaze_data.csv", index=False)


def live_gaze_map(frame):
    img = frame.to_ndarray(format="bgr24")
    GAZE.refresh(img)

    # Exemplo: checando para onde o usuário está olhando
    if GAZE.is_right():
        direction = "Looking right"
    elif GAZE.is_left():
        direction = "Looking left"
    elif GAZE.is_center():
        direction = "Looking center"
    else:
        direction = "Undetected"

    # Desenha texto no frame
    cv2.putText(img, direction, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return av.VideoFrame.from_ndarray(img, format="bgr24")
