from fer import FER
import cv2
import os

# Abrir webcam
video = cv2.VideoCapture(0)
detector = FER()




def print_emotions_formatadas(deteccoes):
    for i, face in enumerate(deteccoes, 1):
        box = face["box"]
        emotions = face["emotions"]

        print(f"\n🔲 Rosto {i}: (x: {box[0]}, y: {box[1]}, largura: {box[2]}, altura: {box[3]})")
        print("😶 Emoções detectadas:")

        for emocao, score in emotions.items():
            print(f"  {emocao.capitalize():<10}: {score:.2f}")

        # Emoção predominante
        emocao_max = max(emotions, key=emotions.get)
        print(f"⭐ Emoção predominante: {emocao_max.capitalize()} ({emotions[emocao_max]:.2f})")


while True:
    ret, frame = video.read()
    if not ret:
        break
    result = detector.detect_emotions(frame)
    clear()
    print_emotions_formatadas(result)
    cv2.imshow("AVBER - Monitoring Expressions", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
