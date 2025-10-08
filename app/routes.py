# app/routes.py

from flask import Blueprint, render_template, request, jsonify, current_app
from . import services
from . import database as db
from app import socketio
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
    """Endpoint de API que retorna a fila E o contador de atendidos."""
    
    # 1. Busca a fila de espera já organizada pelo serviço
    fila_de_espera = services.obter_fila_organizada()
    
    # 2. Busca o total de senhas já atendidas no banco de dados
    total_atendidos = db.contar_atendidos()
    
    # 3. Retorna um único objeto JSON com ambas as informações
    return jsonify({'fila': fila_de_espera, 'atendidos': total_atendidos})


@bp.route('/atender/<int:id_senha>', methods=['POST'])
def atender_senha(id_senha):
    """Marca uma senha como atendida e avisa todos os clientes via WebSocket."""
    sucesso = db.marcar_como_atendido(id_senha)
    
    if sucesso:
        socketio.emit('fila_atualizada', {'message': f'Senha {id_senha} foi atendida.'})
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Senha não encontrada'}), 404
    
# Dentro de app/routes.py
@bp.route('/limpar-fila', methods=['POST'])
def limpar_fila():
    # AQUI: A rota chama a função para apagar os dados do banco
    db.resetar_senhas_diarias()
    
    # E depois avisa a todos em tempo real que a fila mudou
    socketio.emit('fila_atualizada', {'message': 'A fila foi limpa.'})
    
    return jsonify({'status': 'success'}), 200