import streamlit as st
import cv2
import tempfile
import time
from components import *
from streamlit_webrtc import webrtc_streamer
import time

st.set_page_config(layout="wide")
st.title("AVBER - Ads Validation by Emotion Recognition")

# Inicializa estados na sessão
if "TMP_VIDEO_PATH" not in st.session_state:
    st.session_state["TMP_VIDEO_PATH"] = None
if "RUNNING_ANALYSIS" not in st.session_state:
    st.session_state["RUNNING_ANALYSIS"] = False
if "STOP_ANALYSIS" not in st.session_state:
    st.session_state["STOP_ANALYSIS"] = False
if "CONCLUDED_ANALYSIS" not in st.session_state:
    st.session_state["CONCLUDED_ANALYSIS"] = False
if "CANCELED_ANALYSIS" not in st.session_state:
    st.session_state["CANCELED_ANALYSIS"] = False
if "LIVE_EMOTION_ON" not in st.session_state:
    st.session_state["LIVE_EMOTION_ON"] = False

# ====== LIVE EMOTION TEST ======= #
if not st.session_state["LIVE_EMOTION_ON"]:
    if st.button("Live Emotion Map", type="primary"):
        st.session_state["LIVE_EMOTION_ON"] = True
        st.rerun()  # reexecuta para mostrar o webrtc_streamer
else:
    # Inicia o stream
    st.markdown("Live Emotion Test...")
    webrtc_streamer(
        key="emotion-detector",
        video_frame_callback=live_emotion_map,
        media_stream_constraints={
            "video": {"width": {"ideal": 1280}, "height": {"ideal": 720}, "frameRate": {"ideal": 60}},
            "audio": False,
        },
    )

    # Mostra o botão "Parar"
    if st.button("ⓧ Encerrar teste", type="tertiary"):
        st.session_state["LIVE_EMOTION_ON"] = False
        st.rerun()  # reexecuta para voltar ao botão inicial


# Upload de vídeo
video_file = st.file_uploader("Escolha o vídeo da propaganda a ser avaliada.", type=["mp4"])
if video_file:
    st.session_state["TMP_VIDEO_PATH"] = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    with open(st.session_state["TMP_VIDEO_PATH"], "wb") as f:
        f.write(video_file.read())
    st.markdown("🗹 Vídeo carregado.")


# Se vídeo carregado
if st.session_state["TMP_VIDEO_PATH"]:
    col_video, col_info = st.columns([2, 1])  # Layout estilo YouTube

    with col_info:
        # Botões de controle
        if not st.session_state["RUNNING_ANALYSIS"] and not st.session_state["CONCLUDED_ANALYSIS"]:
            if st.button("Iniciar Análise", icon=":material/play_circle:"):
                st.session_state["RUNNING_ANALYSIS"] = True
                st.session_state["STOP_ANALYSIS"] = False
                st.session_state["CANCELED_ANALYSIS"] = False
                st.rerun()

        elif st.session_state["RUNNING_ANALYSIS"]:
            if st.button("Cancelar Análise", icon=":material/stop_circle:", type="primary"):
                st.session_state["CANCELED_ANALYSIS"] = True
                st.session_state["RUNNING_ANALYSIS"] = False
                st.rerun()

        elif st.session_state["CONCLUDED_ANALYSIS"]:
            st.success("Análise finalizada.")
            if st.button("Nova Análise", icon=":material/refresh:"):
                st.session_state.update(
                    {
                        "RUNNING_ANALYSIS": False,
                        "STOP_ANALYSIS": False,
                        "CONCLUDED_ANALYSIS": False,
                        "CANCELED_ANALYSIS": False,
                        "TMP_VIDEO_PATH": None,
                    }
                )
                st.rerun()

        # Espaço para status e progresso
        status_placeholder = st.empty()
        progress_bar = st.progress(0)

    # Coluna de vídeo
    with col_video:
        if st.session_state["RUNNING_ANALYSIS"]:
            st.video(st.session_state["TMP_VIDEO_PATH"], autoplay=True)

# Lógica da análise sincronizada com vídeo
if (
    st.session_state["RUNNING_ANALYSIS"]
    and not st.session_state["CANCELED_ANALYSIS"]
    and not st.session_state["CONCLUDED_ANALYSIS"]
):
    cap_video = cv2.VideoCapture(st.session_state["TMP_VIDEO_PATH"])
    cap_webcam = cv2.VideoCapture(0)
    out = cv2.VideoWriter("data/webcam_output.avi", cv2.VideoWriter_fourcc(*"XVID"), 20.0, (640, 480))

    total_frames = int(cap_video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap_video.get(cv2.CAP_PROP_FPS)
    frame_duration = 1.0 / fps if fps > 0 else 1.0 / 25  # fallback padrão

    current_frame = 0
    prev_time = time.time()

    while cap_video.isOpened():
        if st.session_state["CANCELED_ANALYSIS"]:
            status_placeholder.markdown("🗷 Análise cancelada pelo usuário.")
            break

        ret_vid, frame_vid = cap_video.read()
        ret_cam, frame_cam = cap_webcam.read()

        if not ret_vid or not ret_cam:
            break

        out.write(frame_cam)
        current_frame += 1

        # Atualiza progresso e status
        progress = current_frame / total_frames
        progress_bar.progress(progress)
        status_placeholder.markdown(f"● Capturando reações... {int(progress * 100)}%")

        # Aguarda o tempo correto para o próximo frame (sincronizado com FPS)
        elapsed = time.time() - prev_time
        sleep_time = frame_duration - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)
        prev_time = time.time()

    with col_info:
        st.markdown(f"🗹 Capturando reações... 100%")

    # Libera recursos
    cap_video.release()
    cap_webcam.release()
    out.release()

    if not st.session_state["CANCELED_ANALYSIS"]:

        def update_progress(progress):
            percent = int(progress * 100)
            status_placeholder.markdown(f"🗘 Processando emoções... {percent}%")
            progress_bar.progress(percent)

        process_emotions("data/webcam_output.avi", progress_callback=update_progress)
        with col_info:
            st.markdown(f"🗹 Processando emoções... 100%")

        status_placeholder.markdown("🗘 Processando rastreio ocular...")
        track_gaze("data/webcam_output.avi")
        with col_info:
            st.markdown("🗹 Processando rastreio ocular... 100%")

        status_placeholder.markdown("🗘 Gerando gráficos...")
        gerar_graficos()
        with col_info:
            st.markdown("🗹 Gerando gráficos... 100%")

        st.image("out/emotion_plot.png", caption="Gráfico de Emoções", use_column_width=True)
        st.image("out/heatmap.png", caption="Heatmap Ocular", use_column_width=True)
        status_placeholder.markdown("🗹 Análise concluída!")

        st.session_state["RUNNING_ANALYSIS"] = False
        st.session_state["CONCLUDED_ANALYSIS"] = True
        # progress_bar.progress(0)
