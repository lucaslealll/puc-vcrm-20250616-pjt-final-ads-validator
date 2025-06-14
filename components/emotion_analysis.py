from fer import FER
import pandas as pd
import cv2
import av


def process_emotions(video_path, progress_callback=None):
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(video_path)

    data = []
    frame_num = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
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

        # Atualiza progresso se callback foi passado
        if progress_callback is not None and total_frames > 0:
            progress = frame_num / total_frames
            progress_callback(progress)

    cap.release()
    df = pd.DataFrame(data)
    df.to_csv("data/emotion_analysis.csv", index=False)


def live_emotion_map(frame: av.VideoFrame) -> av.VideoFrame:
    detector = FER(mtcnn=True)

    img = frame.to_ndarray(format="bgr24")

    results = detector.detect_emotions(img)

    for face in results:
        (x, y, w, h) = face["box"]
        emotions = face["emotions"]
        top_emotion = max(emotions, key=emotions.get)
        score = emotions[top_emotion]

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = f"{top_emotion} ({score:.2f})"
        cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return av.VideoFrame.from_ndarray(img, format="bgr24")
