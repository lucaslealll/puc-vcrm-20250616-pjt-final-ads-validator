import streamlit as st
import cv2
import tempfile
from components import *

st.set_page_config(layout="wide")
st.title("AVBER - Ads Validation by Emotion Recognition")

# Upload do vídeo
video_file = st.file_uploader("Escolha o vídeo da propaganda a ser avaliada.", type=["mp4"])
confirm = st.button("Confirmar Vídeo")

# Flags de controle
if "video_confirmed" not in st.session_state:
    st.session_state["video_confirmed"] = False

if confirm and video_file:
    st.session_state["video_confirmed"] = True
    st.session_state["temp_video_path"] = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    with open(st.session_state["temp_video_path"], "wb") as f:
        f.write(video_file.read())

# Exibir frames iniciais após confirmação
if st.session_state["video_confirmed"]:
    st.markdown("✅ Vídeo confirmado. Exibindo frames...")

    cap_video = cv2.VideoCapture(st.session_state["temp_video_path"])
    cap_webcam = cv2.VideoCapture(0)

    ret_vid, frame_vid = cap_video.read()
    ret_cam, frame_cam = cap_webcam.read()

    cap_video.release()
    cap_webcam.release()

    # if ret_vid and ret_cam:
    #     col1, col2 = st.columns([2, 1])
    #     frame_vid_resized = cv2.resize(frame_vid, (1080, 720))
    #     frame_cam_resized = cv2.resize(frame_cam, (640, 480))
    #     col1.image(frame_vid_resized, channels="BGR", caption="Frame da Propaganda")
    #     col2.image(frame_cam_resized, channels="BGR", caption="Webcam (ao vivo)")

    start = st.button("Iniciar Análise")

    if start:
        cap_video = cv2.VideoCapture(st.session_state["temp_video_path"])
        cap_webcam = cv2.VideoCapture(0)
        out = cv2.VideoWriter("data/webcam_output.avi", cv2.VideoWriter_fourcc(*"XVID"), 20.0, (640, 480))

        col1, col2 = st.columns([2, 1])
        video_frame = col1.empty()
        webcam_frame = col2.empty()

        st.markdown("🔴 Capturando reações...")

        while cap_video.isOpened():
            ret_vid, frame_vid = cap_video.read()
            ret_cam, frame_cam = cap_webcam.read()

            if not ret_vid or not ret_cam:
                break

            out.write(frame_cam)

            frame_vid_resized = cv2.resize(frame_vid, (1080, 720))
            frame_cam_resized = cv2.resize(frame_cam, (640, 480))

            video_frame.image(frame_vid_resized, channels="BGR", caption="Vídeo da propaganda")
            webcam_frame.image(frame_cam_resized, channels="BGR", caption="Webcam do usuário")

        cap_video.release()
        cap_webcam.release()
        out.release()

        st.success("🎯 Captura concluída!")

        st.write("🔍 Processando emoções...")
        process_emotions("data/webcam_output.avi")

        st.write("👁️ Processando rastreio ocular...")
        track_gaze("data/webcam_output.avi")

        st.write("📊 Gerando gráficos...")
        gerar_graficos()

        st.image("out/emotion_plot.png", caption="Gráfico de Emoções")
        st.image("out/heatmap.png", caption="Heatmap Ocular")
