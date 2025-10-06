from flask import Flask
from flask_socketio import SocketIO
from config import Config

socketio = SocketIO()

def create_app(config_class=Config):
    """
    Cria e configura a instância do Flask.
    """
    app = Flask(__name__, static_folder='../public', template_folder='../public', static_url_path='')
    app.config.from_object(config_class)

    # Inicialização de módulos
    from . import database
    with app.app_context():
        database.criar_tabela()

    from . import scheduler
    scheduler.configurar_agendamentos()

    # Registro de Rotas
    from . import routes
    app.register_blueprint(routes.bp)

    socketio.init_app(app)
    
    print('Aplicação Flask e o MÓDULO SOCKET.IO foram inicizalizados.')
    return app, socketio