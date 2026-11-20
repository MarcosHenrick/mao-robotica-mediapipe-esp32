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
    

    def contarPontos(
        self,
        lista_ponto,
        imagem=None,
        desenho=False,
        cor=(255, 0, 255),
        raio=7,
        espelhada=True,
        mao_direita=True,
        margem=10,
    ):
        # Mapeamento fixo: ID do ponto da ponta -> estado (0 = inativo, 1 = ativo)
        # 4: dedão | 8: indicador | 12: médio | 16: anelar | 20: mindinho
        pontos_dedos = [4, 8, 12, 16, 20]
        estado_dedos = {ponto_id: 0 for ponto_id in pontos_dedos}

        if not lista_ponto or len(lista_ponto) < 21:
            return estado_dedos

        # Destaca os pontos fixos de cada dedo na imagem, se solicitado
        if desenho and imagem is not None:
            for ponto_id in pontos_dedos:
                _, cx, cy = lista_ponto[ponto_id]
                cv2.circle(imagem, (cx, cy), raio, cor, cv2.FILLED)

        # 1. Ponto 4 (dedão): comparação horizontal em X
        cx_ponta_dedao = lista_ponto[4][1]
        cx_art_dedao = lista_ponto[2][1]
        cx_ref_indicador = lista_ponto[5][1]

        efetivamente_direita = (not mao_direita) if espelhada else mao_direita

        if efetivamente_direita:
            dedao_aberto = (cx_ponta_dedao > cx_art_dedao - margem) and (
                cx_ponta_dedao > cx_ref_indicador - margem
            )
        else:
            dedao_aberto = (cx_ponta_dedao < cx_art_dedao + margem) and (
                cx_ponta_dedao < cx_ref_indicador + margem
            )

        estado_dedos[4] = 1 if dedao_aberto else 0

        # 2. Pontos 8, 12, 16 e 20: comparação vertical em Y (menor Y = mais alto na tela)
        dedos_verticais = [8, 12, 16, 20]
        for id_ponta in dedos_verticais:
            cy_ponta = lista_ponto[id_ponta][2]
            cy_articulacao = lista_ponto[id_ponta - 2][2]

            if cy_ponta < cy_articulacao:
                estado_dedos[id_ponta] = 1
            else:
                estado_dedos[id_ponta] = 0

        return estado_dedos