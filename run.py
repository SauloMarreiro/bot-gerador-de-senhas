import click
from app import services
from app import create_app, socketio
from app.utils import display_startup_info
from config import Config
from waitress import serve

app, socketio = create_app()

@app.cli.command("seed")
@click.argument("count", type=int, default=15)
def seed_db_command(count):
    """Gera um número 'count' de senhas de teste no banco de dados."""
    print(f"Gerando {count} senhas de teste...")
    for i in range(count):
        # Gera algumas senhas preferenciais para variar
        if i % 4 == 0:
            services.gerar_nova_senha(f'Preferencial Teste {i+1}', 'Preferencial')
        else:
            services.gerar_nova_senha(f'Comum Teste {i+1}', 'Comum')
    print(f"{count} senhas geradas com sucesso!")

if __name__ == '__main__':
    display_startup_info()
    socketio.run(app, host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG, allow_unsafe_werkzeug=True)
    