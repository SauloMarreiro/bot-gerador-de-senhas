from app import create_app, socketio
from app.utils import display_startup_info
from config import Config
from waitress import serve

app, socketio = create_app()

if __name__ == '__main__':
    display_startup_info()
    socketio.run(app, host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG, allow_unsafe_werkzeug=True)
    