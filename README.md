<div style="text-align: center;">
    <h1>
        <img src="assets/PUCMinas.ico" width="100" height="100"/>
        <br>
        <b>Visão Computacional e Realidade Misturada</b>
    </h1> 
    <h2><b>AVBER - Ads Validator By Emotional Recognition:</b> <i>Análise de campanhas publicitárias integrada de respostas visuais e emocionais sob a perspectiva cognitiva do espectador</i><h2>
</div>

### **Descrição do Projeto**
- [Leia a descrição completa no Google Docs](https://docs.google.com/document/d/16zR-Yyn3FRSrZcztXzChu3yRixsqHoV_HX5oCLeXQ1Q).

---
### Análise de Atenção em Propagandas
Este projeto tem como objetivo capturar e analisar o comportamento de usuários ao assistirem a uma propaganda em vídeo, utilizando webcam para rastrear emoções e movimentos oculares.

---
### Objetivos
- Exibir uma propaganda em vídeo enquanto captura o rosto do usuário via webcam.
- Rastrear as emoções do espectador ao longo do tempo.
- Rastrear para onde o usuário está olhando na tela.
- Gerar visualizações, como gráficos de emoções e heatmaps.

---
### Tecnologias Utilizadas
| Categoria                | Ferramentas                     |
|--------------------------|----------------------------------|
| **Interface Gráfica**    | Streamlit                       |
| **Processamento de Vídeo** | OpenCV, ffmpeg-python           |
| **Reconhecimento Facial** | FER, DeepFace (opcional)        |
| **Rastreamento Ocular**  | GazeTracking, MediaPipe         |
| **Visualização de Dados** | matplotlib, pandas, numpy       |

- **FER** só funciona com Python 3.6 ou 3.10.
- **FER** requer as bibliotecas: `moviepy==1.0.3`, `tensorflow>=1.7`, `opencv-contrib-python==3.3.0.9`.

---
### Estrutura de Diretórios
```py
.
├── app.py                            # Arquivo principal, controla a execução do sistema.
├── src                               # Contém vídeos de anúncios para análise.
│   ├── ad01 - Twin Lotus Toothpaste - 2003 Thailand.mp4
│   ├── ad02 - Doritos - The New Kid.mp4
│   ├── ad03 - Toyota - Yaris 5s Ad.mp4
│   ├── ad04 - UFC - UFC 100 Face the pain.mp4
│   └── ad05 - Nike - Winner Stays.mp4
├── components                        # Módulos responsáveis pela análise e visualização dos dados.
│   ├── emotion_analysis.py            # Análise das emoções do espectador a partir de vídeos.
│   ├── gaze_tracker.py                # Rastreamento ocular e posição do olhar.
│   ├── __init__.py                    # Inicialização do pacote `components`.
│   ├── utils.py                       # Funções auxiliares.
│   └── visualization.py               # Criação de gráficos e heatmaps.
├── data                               # Dados utilizados na análise (imagens, vídeos, CSVs).
│   ├── ad_0ms_neutral_73.jpg          # Frames de anúncios com emoções neutras.
│   ├── ad_3300ms_happy_52.jpg
│   ├── ad_7650ms_angry_41.jpg
│   ├── cam_0ms_neutral_73.jpg         # Dados de câmeras, imagens com diferentes emoções.
│   ├── cam_3300ms_happy_52.jpg
│   ├── cam_7650ms_angry_41.jpg
│   ├── emotion_analysis.csv           # Dados da análise de emoções.
│   ├── gaze_data.csv                  # Dados sobre a posição do olhar.
│   └── webcam_output.mp4              # Vídeo gerado pela webcam durante o processo.
├── LICENSE                            # Licença do projeto.
├── out                                # Resultados da análise (gráficos e heatmaps).
│   ├── emotion_plot.png               # Gráfico das emoções detectadas.
│   └── heatmap.png                    # Heatmap do rastreamento ocular.
├── README.md                          # Documentação do projeto.
├── requirements_py310_fer.txt         # Dependências para Python 3.10 e análise de emoções.
├── requirements_py310_pygaze.txt      # Dependências para Python 3.10 e rastreamento ocular.
├── requirements_py312_EyeTracking.txt # Dependências para Python 3.12 (EyeTracking).
├── requirements.txt                   # Dependências gerais do projeto.
└── test                               # Testes unitários do sistema.
    ├── test_FER.py                    # Testes do módulo de análise de emoções.
    └── test_GazeTracking.py           # Testes do módulo de rastreamento ocular.

11 diretórios, 36 arquivos
```

---
### Como Executar
1. Clone o repositório:
    ```bash
    git clone https://github.com/seuusuario/projeto_analise_prop.git
    cd projeto_analise_prop
    ```

2. Instale os requisitos:
    ```bash
    pip install -r requirements.txt
    ```

3. Execute o app:
    ```bash
    streamlit run app.py
    ```

---
### Resultados Esperados
- Captura sincronizada do vídeo e webcam
- Detecção de emoções frame a frame
- Rastreamento de onde o usuário está olhando
- Gráfico com as emoções predominantes
- Heatmap com regiões mais visualizadas do vídeo

---
### Referências

- **DeepFace**: https://github.com/serengil/deepface
- **FER**: https://github.com/justinshenk/fer
- **MediaPipe Face Mesh**: https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/face_mesh.md
- **GazeTracking**: https://github.com/antoinelame/GazeTracking

---
### Créditos
Projeto acadêmico para fins de pesquisa e prototipagem de rastreamento atencional.
