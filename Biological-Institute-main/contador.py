import cv2
import numpy as np

# Vamos redefinir o código para incluir a lógica de contagem baseada no tamanho dos pontos
#tick_larvae_counter
# Carrega a imagem novamente
imagem = cv2.imread('larvas.jpeg')

# Converte para escala de cinza e aplica threshold
cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(cinza, 127, 255, cv2.THRESH_BINARY_INV)

# Encontra contornos na imagem
contornos, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Calcula a área média dos contornos encontrados
areas = [cv2.contourArea(c) for c in contornos]
area_media = np.mean(areas)

# Inicializa o contador
contador_total = 0

# Define o limiar para o tamanho do ponto como 60%% da área média
limiar_tamanho = area_media * 1.6

# Verifica cada contorno e incrementa o contador apropriadamente
for contorno in contornos:
    area_contorno = cv2.contourArea(contorno)
    (x, y), raio = cv2.minEnclosingCircle(contorno)
    centro = (int(x), int(y))
    raio = int(raio)
    
    # Se a área do contorno for maior do que 70% da média, conta como 2
    if area_contorno > limiar_tamanho:
        contador_total += 2
    else:
        contador_total += 1

    # Desenha um círculo vermelho em volta do ponto
    cv2.circle(imagem, centro, raio, (0, 0, 255), 2)

# Adiciona a contagem total na imagem
posicao_texto = (10, imagem.shape[0] - 10)  # posição no canto inferior esquerdo
cv2.putText(imagem, f"Total: {contador_total}", posicao_texto, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# Salva a imagem com os círculos desenhados e a contagem total
caminho_nova_imagem = 'resultado_contagem_total.jpeg'
cv2.imwrite(caminho_nova_imagem, imagem)

caminho_nova_imagem