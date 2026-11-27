import cv2
import DetectorMaos
from ComunicacaoESP import ComunicacaoESP

# Ajuste a porta: Windows "COM3", Linux "/dev/ttyUSB0", Mac "/dev/cu.usbserial-XXXX"
PORTA_ESP32 = "COM6"

detector = DetectorMaos.DetectorMaos()
esp32 = ComunicacaoESP(porta=PORTA_ESP32)


def main():

    # Capturar o vídeo da webcam:
    cap = cv2.VideoCapture(0)

    while True:

        # Obter a imagem da webcam:
        ok, imagem = cap.read()
        if not ok:
            break

        # Espelhar imagem:
        imagem = cv2.flip(imagem, 1)

        # Detectar mãos e desenhar:
        imagem = detector.encontrarMaos(imagem)

        # Lista com os pontos das mãos detectadas:
        lista_pontos = detector.encontrarPontos(imagem)

        # Estado de cada dedo:
        dedos = detector.contarPontos(lista_pontos, imagem=imagem, desenho=True)
        total_dedos = sum(dedos.values())

        print(f"Dedos levantados: {total_dedos} -> {dedos}")

        # Enviar para o ESP32 (só envia quando houver mudança):
        esp32.enviar(dedos)

        # Mostrar a imagem na tela:
        cv2.imshow("window", imagem)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    esp32.fechar()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
