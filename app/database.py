import sqlite3
from config import Config
from datetime import datetime

def get_db_conn():
    """Cria uma conexão com o banco de dados."""
    conn = sqlite3.connect(Config.DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    """Cria a tabela de senhas se ela não existir."""
    try:
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS senhas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL,
                numero_formatado TEXT NOT NULL UNIQUE,
                status TEXT DEFAULT 'aguardando',
                criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        if conn:
            conn.close()
    print("Tabela 'senhas' verificada/criada com sucesso.")


def adicionar_senha(nome, tipo):
    """Adiciona uma nova senha ao banco de dados e a retorna."""
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        prefixo = 'P' if tipo.startswith('P') else 'C'
        cursor.execute(
            "SELECT numero_formatado FROM senhas WHERE tipo LIKE ? ORDER BY id DESC LIMIT 1",
            (prefixo + '%',)
        )
        ultima_senha = cursor.fetchone()
        novo_numero = int(ultima_senha['numero_formatado'][1:]) + 1 if ultima_senha else 1
        senha_gerada = f"{prefixo}{str(novo_numero).zfill(3)}"
        cursor.execute(
            "INSERT INTO senhas (nome, tipo, numero_formatado) VALUES (?, ?, ?)",
            (nome, tipo, senha_gerada)
        )
        conn.commit()
        id_inserido = cursor.lastrowid
        return {"id": id_inserido, "numero_formatado": senha_gerada}
    finally:
        if conn:
            conn.close()

def get_senhas_por_tipo(prefixo_tipo):
    """Busca todas as senhas 'aguardando' de um determinado tipo (C ou P)."""
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM senhas WHERE status = 'aguardando' AND tipo "
        if prefixo_tipo == 'P':
            query += "LIKE 'P%'"
        else:
            query += "NOT LIKE 'P%'"
        query += " ORDER BY id ASC"
        cursor.execute(query)
        senhas = cursor.fetchall()
        return senhas
    finally:
        if conn:
            conn.close()

def resetar_senhas_diarias():
    """Deleta todas as senhas da tabela."""
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM senhas")
        conn.commit()
        print(f"Banco de dados de senhas foi limpo às {datetime.now().strftime('%H:%M:%S')}.")
    finally:
        if conn:
            conn.close()
            
def marcar_como_atendido(id_senha):
    """Muda o status de uma senha de 'aguardando' para 'atendido'."""
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE senhas SET status = 'atendido' WHERE id = ?",
            (id_senha,)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        if conn:
            conn.close()
            
def resetar_senhas_diarias():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM senhas")
    conn.commit()
    conn.close()