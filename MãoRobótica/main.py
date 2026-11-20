import cv2
import DetectorMaos

detector = DetectorMaos.DetectorMaos()

def main():

    #Capturar o vídeo da webcam:
    cap = cv2.VideoCapture(0)

    #Realizar a captura:
    while True:

        #Obter a imagem da webcam:
        _, imagem = cap.read()

        #Rotacionar tela:
        imagem = cv2.flip(imagem, 1)

        # Detectar imagem das maos
        imagem = detector.encontrarMaos(imagem)
        
        # Lista com os pontos das mãos detectadas:
        lista_pontos = detector.encontrarPontos(imagem)
        
                
        if lista_pontos:
            print(lista_pontos)

        #Mostrar a imagem na tela:
        cv2.imshow("window", imagem)
        #Tempo de atualização da imagem:

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()