import streamlit as st
import cv2
import tempfile
from components import *

st.title("Análise de Atenção em Propagandas")

video_file = st.file_uploader("Escolha o vídeo da propaganda", type=["mp4"])
start = st.button("Iniciar Análise")

if video_file and start:
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video.write(video_file.read())

    cap_video = cv2.VideoCapture(temp_video.name)
    cap_webcam = cv2.VideoCapture(0)
    out = cv2.VideoWriter("data/webcam_output.avi", cv2.VideoWriter_fourcc(*"XVID"), 20.0, (640, 480))

    stframe = st.empty()
    st.markdown("Gravando...")

    while cap_video.isOpened():
        ret_vid, frame_vid = cap_video.read()
        ret_cam, frame_cam = cap_webcam.read()

        if not ret_vid or not ret_cam:
            break

        out.write(frame_cam)
        frame_vid_resized = cv2.resize(frame_vid, (640, 480))
        stframe.image(frame_vid_resized, channels="BGR")

    cap_video.release()
    cap_webcam.release()
    out.release()

    st.success("Captura concluída.")

    st.write("Processando emoções...")
    process_emotions("data/webcam_output.avi")

    st.write("Processando rastreio ocular...")
    track_gaze("data/webcam_output.avi")

    st.write("Gerando gráficos...")
    gerar_graficos()

    st.image("out/emotion_plot.png", caption="Gráfico de Emoções")
    st.image("out/heatmap.png", caption="Heatmap Ocular")
