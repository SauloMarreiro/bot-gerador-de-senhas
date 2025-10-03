import socket
import qrcode
from config import Config

def get_local_ip():
    """Encontra o IP local da máquina para fácil acesso na rede."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def display_startup_info():
    """Mostra o QR Code e a URL de acesso no terminal."""
    ip_local = get_local_ip()
    url = f"http://{ip_local}:{Config.PORT}"
    print("\n" + "="*50)
    print("Escaneie o QR Code ou acesse a URL abaixo:")
    qrcode.generate(url, version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, output=lambda s: print(s, end=''))
    print(f"Servidor Local: {url}")
    print("="*50 + "\n")