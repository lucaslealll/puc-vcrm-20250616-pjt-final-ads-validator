import streamlit as st
import cv2
import tempfile
import time
from components import *

st.set_page_config(layout="wide")
st.title("AVBER - Ads Validation by Emotion Recognition")

if "temp_video_path" not in st.session_state:
    st.session_state["temp_video_path"] = None

if "running_analysis" not in st.session_state:
    st.session_state["running_analysis"] = False

if "stop_analysis" not in st.session_state:
    st.session_state["stop_analysis"] = False

# Upload do vídeo
video_file = st.file_uploader("Escolha o vídeo da propaganda a ser avaliada.", type=["mp4"])

if video_file:
    st.session_state["temp_video_path"] = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    with open(st.session_state["temp_video_path"], "wb") as f:
        f.write(video_file.read())

if st.session_state["temp_video_path"]:
    st.markdown("✅ Vídeo carregado. Reproduza abaixo com áudio:")
    st.video(st.session_state["temp_video_path"])

col1, col2 = st.columns(2)

if not st.session_state["running_analysis"]:
    if col1.button("Iniciar Análise"):
        st.session_state["running_analysis"] = True
        st.session_state["stop_analysis"] = False
elif st.session_state["running_analysis"]:
    if col2.button("Cancelar Análise"):
        st.session_state["stop_analysis"] = True

status_placeholder = st.empty()
progress_bar = st.progress(0)

if st.session_state["running_analysis"]:
    cap_video = cv2.VideoCapture(st.session_state["temp_video_path"])
    cap_webcam = cv2.VideoCapture(0)
    out = cv2.VideoWriter("data/webcam_output.avi", cv2.VideoWriter_fourcc(*"XVID"), 20.0, (640, 480))

    total_frames = int(cap_video.get(cv2.CAP_PROP_FRAME_COUNT))
    current_frame = 0

    while cap_video.isOpened():
        if st.session_state["stop_analysis"]:
            status_placeholder.markdown("⚠️ Análise cancelada pelo usuário.")
            break

        ret_vid, frame_vid = cap_video.read()
        ret_cam, frame_cam = cap_webcam.read()

        if not ret_vid or not ret_cam:
            break

        out.write(frame_cam)
        current_frame += 1

        progress = current_frame / total_frames
        progress_bar.progress(progress)
        status_placeholder.markdown(f"🔴 Capturando reações... {int(progress * 100)}%")

        # Aguarda 0.05s para permitir atualização da interface
        time.sleep(0.05)

    cap_video.release()
    cap_webcam.release()
    out.release()

    if not st.session_state["stop_analysis"]:
        status_placeholder.markdown("🎯 Captura concluída! Processando emoções...")
        process_emotions("data/webcam_output.avi")

        status_placeholder.markdown("👁️ Processando rastreio ocular...")
        track_gaze("data/webcam_output.avi")

        status_placeholder.markdown("📊 Gerando gráficos...")
        gerar_graficos()

        st.image("out/emotion_plot.png", caption="Gráfico de Emoções")
        st.image("out/heatmap.png", caption="Heatmap Ocular")
        status_placeholder.markdown("✅ Análise concluída!")

    st.session_state["running_analysis"] = False
    st.session_state["stop_analysis"] = False
    progress_bar.progress(0)
