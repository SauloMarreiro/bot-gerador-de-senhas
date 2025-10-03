from flask import Flask
from config import Config

def create_app(config_class=Config):
    """
    Cria e configura a instância do Flask.
    """
    app = Flask(__name__, static_folder='../public', template_folder='../public')
    app.config.from_object(config_class)

    # --- REGISTRO DE COMPONENTES ---
    # (Aqui vamos adicionar o banco de dados, as rotas, etc. no futuro)
    
    # Exemplo (será adicionado em features futuras):
    # from . import database
    # database.init_app(app)
    
    # from . import routes
    # app.register_blueprint(routes.bp)

    print("Aplicação Flask criada com sucesso.")
    return app