from fer import FER
import pandas as pd
import cv2


def process_emotions(video_path):
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(video_path)

    data = []
    frame_num = 0
    fps = cap.get(cv2.CAP_PROP_FPS)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result = detector.detect_emotions(frame)
        timestamp = frame_num / fps

        if result:
            dominant = max(result[0]["emotions"], key=result[0]["emotions"].get)
        else:
            dominant = "none"

        data.append({"frame": frame_num, "time": timestamp, "emotion": dominant})
        frame_num += 1

    cap.release()
    df = pd.DataFrame(data)
    df.to_csv("data/emotion_analysis.csv", index=False)
