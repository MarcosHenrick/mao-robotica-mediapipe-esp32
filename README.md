# Configuração e Execução

Guia rápido para configurar o ambiente e executar o projeto localmente.

## Pré-requisitos

* **Python 3.10 a 3.12** instalado *(projeto testado e validado em **Python 3.11**; versões muito recentes como 3.13+ podem não ser compatíveis com `mediapipe==0.10.14`)*.
* **Webcam** conectada e livre (não utilizada por outros programas).

## Passo a Passo

### 1. Criar e ativar o ambiente virtual (`.venv`)

O ambiente virtual (`venv`) usa o interpretador Python já instalado na sua máquina e inicia vazio — por isso é obrigatório criar o ambiente e instalar as bibliotecas antes de executar o código.

* **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
  *(Caso tenha mais de uma versão do Python instalada no Windows e queira usar uma específica, como a 3.11, utilize: `py -3.11 -m venv .venv`)*

* **Windows (Git Bash):**
  ```bash
  python -m venv .venv
  source .venv/Scripts/activate
  ```

* **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
  *(Para especificar uma versão instalada, como Python 3.11, utilize: `python3.11 -m venv .venv`)*

### 2. Instalar as bibliotecas necessárias

Com o ambiente virtual ativado (`(.venv)` visível no terminal), instale as dependências:

```bash
python -m pip install --upgrade pip
pip install "mediapipe==0.10.14" opencv-python
```

### 3. Executar o código

Com o ambiente ativado e o interpretador configurado no seu editor para o `.venv`, execute:

```bash
python "MãoRobótica/main.py"
```

* Pressione a tecla **`q`** na janela do vídeo para encerrar o programa.