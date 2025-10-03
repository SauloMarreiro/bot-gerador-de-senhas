from app import create_app
from app.utils import display_startup_info
from config import Config
from waitress import serve

app = create_app()

if __name__ == '__main__':
    display_startup_info()

    if Config.DEBUG:
        app.run(host='0.0.0.0', port=Config.PORT, debug=True)
    else:
        serve(app, host='0.0.0.0', port=Config.PORT)