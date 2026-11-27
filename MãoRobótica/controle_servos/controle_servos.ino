// Controle de 5 servos pelo ESP32 de acordo com o estado dos dedos
// Recebe pela serial linhas no formato: "1,0,1,1,0\n"
// Ordem: dedão, indicador, médio, anelar, mindinho
// Biblioteca necessária: ESP32Servo (Gerenciador de Bibliotecas da Arduino IDE)

#include <Servo.h>

const int NUM_DEDOS = 5;

// Pinos dos servos: dedão, indicador, médio, anelar, mindinho
const int pinosServo[NUM_DEDOS] = {D1};

// Ângulos (ajuste conforme sua montagem mecânica)
const int ANGULO_FECHADO = 0;
const int ANGULO_ABERTO  = 90;

Servo servos[NUM_DEDOS];

void setup() {
  Serial.begin(115200);

  for (int i = 0; i < NUM_DEDOS; i++) {
    servos[i].setPeriodHertz(50);
    servos[i].attach(pinosServo[i], 500, 2400);
    servos[i].write(ANGULO_FECHADO);
  }
}

void loop() {
  if (Serial.available()) {
    String linha = Serial.readStringUntil('\n');
    linha.trim();

    int estado[NUM_DEDOS];
    int idx = 0;
    int inicio = 0;

    // Separa "1,0,1,1,0" em valores
    for (int i = 0; i <= (int)linha.length() && idx < NUM_DEDOS; i++) {
      if (i == (int)linha.length() || linha[i] == ',') {
        estado[idx++] = linha.substring(inicio, i).toInt();
        inicio = i + 1;
      }
    }

    if (idx == NUM_DEDOS) {
      for (int i = 0; i < NUM_DEDOS; i++) {
        servos[i].write(estado[i] ? ANGULO_ABERTO : ANGULO_FECHADO);
      }
    }
  }
}
