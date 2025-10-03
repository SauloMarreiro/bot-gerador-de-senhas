# app/routes.py

from flask import Blueprint, render_template, request, jsonify, current_app
from . import services

# Criamos um "Blueprint", uma forma de organizar um grupo de rotas relacionadas.
bp = Blueprint('main', __name__)

@bp.route("/")
def index():
    """Serve a página inicial com o formulário para gerar senhas."""
    # Usamos send_from_directory para servir o arquivo estático index.html
    return current_app.send_static_file('index.html')

@bp.route("/gerar", methods=["POST"])
def gerar_senha():
    """Recebe os dados do formulário, gera a senha e mostra a página de resultado."""
    nome = request.form.get('nome')
    tipo = request.form.get('tipo')

    # Chama a camada de serviço para fazer o trabalho pesado
    nova_senha_info = services.gerar_nova_senha(nome, tipo)

    if nova_senha_info is None:
        return "Erro: Nome e tipo são obrigatórios.", 400

    # Renderiza o template de resultado, passando as informações da nova senha
    return render_template('resultado.html', **nova_senha_info)

@bp.route("/painel")
def painel():
    """Serve a página do painel de senhas."""
    return current_app.send_static_file('painel.html')

@bp.route("/api/painel")
def api_painel():
    """Endpoint de API que retorna a fila de senhas em formato JSON."""
    # Chama a camada de serviço para obter e organizar a fila
    fila = services.obter_fila_organizada()
    return jsonify(fila)