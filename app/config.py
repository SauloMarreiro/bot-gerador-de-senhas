import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Classe para centralizar as configurações da aplicação."""
    SECRET_KEY = os.environ.get('SECRET_KEY')

    PORT = 3000
    DATABASE_NAME = "senhas.db"

    DEBUG = os.environ.get('FLASK_DEBUG') == 'True'