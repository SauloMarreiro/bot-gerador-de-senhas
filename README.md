# Bot Gerador de Senhas com Painel Web

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.2-black?style=for-the-badge&logo=flask)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge)

_Um sistema de gerenciamento de filas e senhas acessado via QR Code, com painel de visualização e administração em tempo real._

---

### Visão Geral

Este projeto é uma aplicação web construída em Python e Flask que fornece um sistema completo para geração e chamada de senhas de atendimento, ideal para pequenos estabelecimentos, consultórios ou eventos.

### ✨ Funcionalidades Principais

- **Geração de Senhas:** Atendimento Comum e Preferencial.
- **Painel em Tempo Real:** Visualização da fila que atualiza automaticamente para todos os usuários conectados via WebSockets.
- **Administração do Painel:**
    - Marcar senhas como "atendidas".
    - Limpar toda a fila para testes ou reinício do dia.
- **QR Code de Acesso:** Geração de QR Code no terminal para acesso rápido à página de geração de senhas.
- **Impressão Otimizada:** Layout de impressão especial para impressoras térmicas de 58mm.

### 🛠️ Tecnologias Utilizadas

- **Backend:** Python, Flask, Flask-SocketIO, Waitress
- **Banco de Dados:** SQLite
- **Frontend:** HTML5, CSS3 (Flexbox), JavaScript
- **Utilitários:** `qrcode`, `schedule`, `python-dotenv`

### 🔌 Documentação da API

A aplicação expõe os seguintes endpoints de API para o frontend.

#### Listar Senhas na Fila
- **URL:** `/api/painel`
- **Método:** `GET`
- **Descrição:** Retorna um array de objetos JSON, cada objeto representando uma senha na fila com o status 'aguardando', já na ordem de chamada.
- **Resposta de Sucesso (200):**
  ```json
  [
    {
      "id": 1,
      "nome": "Saulo",
      "numero_formatado": "P001",
      "status": "aguardando",
      "tipo": "Preferencial Idoso",
      "criado_em": "..."
    }
  ]

### 🚀 Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

**1. Clone o Repositório**
```bash
git clone [https://github.com/SauloMarreiro/bot-gerador-de-senhas.git](https://github.com/SauloMarreiro/bot-gerador-de-senhas.git)
cd bot-gerador-de-senhas
```

**2. Crie e Ative o Ambiente Virtual**
Isso cria um ambiente Python isolado para o projeto.

* No Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
* No macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**3. Instale as Dependências**
Este comando lê o arquivo `requirements.txt` e instala todas as bibliotecas necessárias.
```bash
pip install -r requirements.txt
```

**4. Configure as Variáveis de Ambiente**
Este projeto usa um arquivo `.env` para gerenciar chaves secretas e configurações de ambiente. Nós fornecemos um arquivo de exemplo chamado `.env.example`.

* **Copie o arquivo de exemplo** para criar seu próprio arquivo de configuração local.
    * No Windows:
        ```bash
        copy .env.example .env
        ```
    * No macOS/Linux:
        ```bash
        cp .env.example .env
        ```

* **Gere uma `SECRET_KEY`:** O arquivo `.env` precisa de uma chave secreta para o Flask. Execute o comando abaixo no seu terminal para gerar uma chave segura:
    ```bash
    python -c 'import secrets; print(secrets.token_hex(24))'
    ```

* **Edite o arquivo `.env`:** Abra o arquivo `.env` que você acabou de criar. Ele terá o seguinte conteúdo:
    ```env
    SECRET_KEY='coloque-aqui-a-chave-segura-gerada'
    FLASK_DEBUG=True
    ```
    **Copie a chave** que você gerou no passo anterior e **cole no lugar de `'coloque-aqui-a-chave-segura-gerada'`**. Salve o arquivo.

**5. Execute a Aplicação**
Com tudo configurado, inicie o servidor:
```bash
python run.py
```
Após a execução, um QR Code e a URL de acesso local serão exibidos no terminal.
