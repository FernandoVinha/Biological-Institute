import cv2
import numpy as np

def processar_frame(frame):
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(cinza, 127, 255, cv2.THRESH_BINARY_INV)
    contornos, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    pontos = [cv2.minEnclosingCircle(c)[0] for c in contornos if cv2.contourArea(c) > 5]
    return np.array(pontos, dtype=np.float32).reshape(-1, 1, 2)

# Inicializa a captura de vídeo
cap = cv2.VideoCapture('larvas_video.mp4')

# Leitura do primeiro frame
ret, frame_anterior = cap.read()
pontos_anteriores = processar_frame(frame_anterior)
contador_parados = 0
contador_moveis = 0

# Criação de parâmetros para o Lucas-Kanade
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Loop para cada quadro do vídeo
while True:
    ret, frame = cap.read()
    if not ret:
        break

    pontos_atuais = processar_frame(frame)
    pontos_anteriores, st, _ = cv2.calcOpticalFlowPyrLK(frame_anterior, frame, pontos_anteriores, None, **lk_params)

    # Contagem dos pontos
    for i, (novo, antigo) in enumerate(zip(pontos_atuais, pontos_anteriores)):
        a, b = novo.ravel()
        c, d = antigo.ravel()
        if np.linalg.norm((a - c, b - d)) < 2:
            contador_parados += 1
        else:
            contador_moveis += 1

    frame_anterior = frame.copy()
    pontos_anteriores = pontos_atuais.copy()

    # Exibe a contagem
    cv2.putText(frame, f"Parados: {contador_parados}, Moveis: {contador_moveis}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura de vídeo e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()
