

import time
import serial


class ComunicacaoESP:
    """Envia o estado dos dedos para o ESP32 pela porta serial (USB)."""

    # Ordem fixa dos dedos na mensagem: dedão, indicador, médio, anelar, mindinho
    ORDEM_DEDOS = [4, 8, 12, 16, 20]

    def __init__(self, porta="COM6", baud=115200, espera_reset=2):
        self.porta = porta
        self.baud = baud
        self.ultima_mensagem = None
        self.conexao = None

        try:
            self.conexao = serial.Serial(porta, baud, timeout=1)
            # O ESP32 costuma reiniciar ao abrir a serial
            time.sleep(espera_reset)
            print(f"Conectado ao ESP32 em {porta}")
        except serial.SerialException as erro:
            print(f"Não foi possível abrir {porta}: {erro}")

    @property
    def conectado(self):
        return self.conexao is not None and self.conexao.is_open

    def enviar(self, estado_dedos):
        """Recebe o dicionário {4: 0/1, 8: 0/1, ...} e envia só quando mudar."""
        if not self.conectado:
            return

        valores = [str(estado_dedos[id_ponta]) for id_ponta in self.ORDEM_DEDOS]
        mensagem = ",".join(valores) + "\n"   # ex: "1,0,0,1,1\n"

        if mensagem != self.ultima_mensagem:
            self.conexao.write(mensagem.encode())
            self.ultima_mensagem = mensagem
            print(f"Enviado ao ESP32: {mensagem.strip()}")

    def fechar(self):
        if self.conectado:
            self.conexao.write(b"0,0,0,0,0\n")  # servos em repouso
            self.conexao.close()
