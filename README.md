# PUC - VISÃO COMPUTACIONAL E REALIDADE MISTURADA

**AVBER - Ads Validator By Emotional Recognition:** _análise de campanhas publicitárias integrada de respostas visuais e emocionais sob a perspectiva cognitiva do espectador_

- Descrição do projeto: [Google Docs](https://docs.google.com/document/d/16zR-Yyn3FRSrZcztXzChu3yRixsqHoV_HX5oCLeXQ1Q)

---
### Análise de Atenção em Propagandas
Este projeto tem como objetivo capturar e analisar o comportamento de usuários ao assistirem a uma propaganda em vídeo, utilizando webcam para rastrear emoções e movimentos oculares.

---
### Objetivos
- Exibir uma propaganda em vídeo enquanto captura o rosto do usuário via webcam
- Rastrear as emoções ao longo do tempo
- Rastrear para onde o usuário está olhando na tela
- Gerar visualizações como gráficos de emoções e heatmaps

---
### Tecnologias Utilizadas
| Categoria                | Ferramentas                     |
|--------------------------|----------------------------------|
| Interface Gráfica        | Streamlit                       |
| Processamento de Vídeo   | OpenCV, ffmpeg-python           |
| Reconhecimento Facial    | FER, DeepFace (opcional)        |
| Rastreamento Ocular      | GazeTracking, MediaPipe         |
| Visualização de Dados    | matplotlib, pandas, numpy       |

* FER só funciona com python 3.6

---
### Estrutura de Diretórios
```py
    puc-vcrm-ads-validator/          
    ├── app.py                      # Interface principal com Streamlit
    ├── requirements.txt            # Bibliotecas necessárias
    ├── utils/                       
    │ ├── emotion_analysis.py       # Análise de emoções com FER/DeepFace
    │ ├── gaze_tracking.py          # Rastreamento ocular com GazeTracking
    │ └── visualization.py          # Geração de gráficos/heatmaps
    ├── data/                        
    │ ├── webcam_output.avi         # Gravação da webcam (gerado)
    │ ├── emotion_analysis.csv      # Dados de emoções (gerado)
    │ └── gaze_data.csv             # Dados de rastreio ocular (gerado)
    ├── out/                      
    │ ├── emotion_plot.png          # Gráfico de emoções (gerado)
    │ └── heatmap.png               # Heatmap de regiões visualizadas (gerado)
    └── README.md                    
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

- DeepFace: https://github.com/serengil/deepface
- FER: https://github.com/justinshenk/fer
- MediaPipe Face Mesh: https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/face_mesh.md
- GazeTracking: https://github.com/antoinelame/GazeTracking

---
### Créditos
Projeto acadêmico para fins de pesquisa e prototipagem de rastreamento atencional.
