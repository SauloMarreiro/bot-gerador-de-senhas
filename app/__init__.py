from flask import Flask
from config import Config

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

    print("Aplicação Flask criada com sucesso.")
    return app