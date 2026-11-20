import cv2
import mediapipe as mp

class DetectorMaos:

    def __init__(self, modo=False, max_maos = 1, deteccao_confianca=0.5, rastreio_confianca=0.5, cor_pontos=(0, 0, 255), cor_conexoes=(0, 0, 255)):

        self.modo = modo
        self.max_maos = max_maos
        self.deteccao_confianca = deteccao_confianca
        self.rastreio_confianca = rastreio_confianca
        self.cor_pontos = cor_pontos
        self.cor_conexoes = cor_conexoes


        # Inicializar o módulo de detecção de mãos do MediaPipe:
        self.mp_maos = mp.solutions.hands
        self.maos = self.mp_maos.Hands(
            static_image_mode=self.modo,
            max_num_hands=self.max_maos,
            min_detection_confidence=self.deteccao_confianca,
            min_tracking_confidence=self.rastreio_confianca
        )
        self.mp_desenho = mp.solutions.drawing_utils

        # Função para detectar pontos nas mãos na imagem:
        self.desenho_mp = mp.solutions.drawing_utils

        #Configurações desenho dos pontos:
        self.desenho_cofig_pontos = self.desenho_mp.DrawingSpec(color=self.cor_pontos) 

        # Configurações do desenho das conexões:
        self.desenho_config_conexoes = self.desenho_mp.DrawingSpec(color=self.cor_conexoes)

    def encontrarMaos(self, imagem, desenho=True):

        # COnverter a imagem de BGR para RGB:
        imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

        # Imagem onvertida para o detector:
        self.resultados = self.maos.process(imagem_rgb)
        
        # Verificar se há mãos detectadas:
        if self.resultados.multi_hand_landmarks:
            for ponto in self.resultados.multi_hand_landmarks:
                if desenho:
                    
                    # Desenhar os pontos e conexões das mãos na imagem:
                    self.mp_desenho.draw_landmarks(
                        imagem, # Imagem de captura
                        ponto, # Pontos das mãos detectadas
                        self.mp_maos.HAND_CONNECTIONS, # Conexões das mãos
                        self.desenho_cofig_pontos, # Configuração cor dos pontos
                        self.desenho_config_conexoes # Configuração cor das conexõesxx
                    )
    
        return imagem
    
    def encontrarPontos(self, imagem, mao_num=0, desenho=True, cor=(255, 0, 255), raio=7):
        
        # Lista de pontos detectados
        lista_ponto = []
        
        # Verificar se alguma mão foi detectada
        if self.resultados.multi_hand_landmarks:
            # Obter pontos da mão especificada:
            
            mao = self.resultados.multi_hand_landmarks[mao_num]
            
            # Obter informaçoes dos pontos da mão:
            for id, ponto in enumerate(mao.landmark):
                
                # Obter dimensões da imagem:
                altura, largura, _ = imagem.shape
                
                # Transformar a posição do ponto de proporcional para pixel:
                cx, cy = int(ponto.x * largura), int(ponto.y * altura)
                
                # Adiionar os pontos na lista:
                lista_ponto.append([id, cx, cy])
                
        return lista_ponto
    
    def contarPontos(self, lista_ponto, imagem=None, desenho=False, cor=(255, 0, 255), raio=7):
            dedos_levantados = []

            if not lista_ponto:
                return dedos_levantados

            dedos = [8, 12, 16, 20]  # Pontas: indicador, médio, anelar, mindinho

            # Destaca opcionalmente as pontas dos dedos na imagem
            if desenho and imagem is not None:
                for ponta_id in dedos:
                    _, cx, cy = lista_ponto[ponta_id]
                    cv2.circle(imagem, (cx, cy), raio, cor, cv2.FILLED)

            # Compara altura (cy -> índice 2): ponta acima da articulação intermediária (id - 2)
            for id_ponta in dedos:
                cy_ponta = lista_ponto[id_ponta][2]
                cy_articulacao = lista_ponto[id_ponta - 2][2]

                if cy_ponta < cy_articulacao:
                    dedos_levantados.append(1)
                else:
                    dedos_levantados.append(0)

            return dedos_levantados

                
            
