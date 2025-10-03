import schedule
import time
import threading
from . import database as db

def rodar_agendamentos():
    """Loop infinito que verifica e executa tarefas pendentes."""
    while True:
        schedule.run_pending()
        time.sleep(60) # Verifica a cada 60 segundos

def configurar_agendamentos():
    """Configura todas as tarefas que devem ser executadas periodicamente."""
    print("Agendador configurado: Reset de senhas às 12:00 e 17:00.")
    schedule.every().day.at("12:00").do(db.resetar_senhas_diarias)
    schedule.every().day.at("17:00").do(db.resetar_senhas_diarias)

    # Inicia o loop de agendamento em uma thread separada para não bloquear o app
    daemon_thread = threading.Thread(target=rodar_agendamentos, daemon=True)
    daemon_thread.start()