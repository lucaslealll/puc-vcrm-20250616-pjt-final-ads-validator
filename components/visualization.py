import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def generate_graphs():
    # Emoções
    df_emotion = pd.read_csv("data/emotion_analysis.csv")
    emotion_counts = df_emotion["emotion"].value_counts()

    plt.figure(figsize=(8, 5))
    emotion_counts.plot(kind="bar", color="steelblue")
    plt.title("Distribuição de Emoções Detectadas")
    plt.ylabel("Número de Frames")
    plt.tight_layout()
    plt.savefig("out/emotion_plot.png")
    plt.close()

    # Heatmap (simples) com contagem de direções do olhar
    df_gaze = pd.read_csv("data/gaze_data.csv")
    counts = (
        df_gaze["direction"].value_counts().reindex(["left", "center", "right", "blinking", "unknown"], fill_value=0)
    )

    plt.figure(figsize=(6, 4))
    sns.heatmap(
        counts.values.reshape(1, -1),
        annot=True,
        xticklabels=counts.index,
        yticklabels=["Olhar"],
        cmap="YlOrRd",
        fmt="d",
    )
    plt.title("Heatmap de Direções do Olhar")
    plt.savefig("out/heatmap.png")
    plt.close()
