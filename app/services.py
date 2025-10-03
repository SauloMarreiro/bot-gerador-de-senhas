from . import database as db

def gerar_nova_senha(nome, tipo):
    """
    Serviço para coordenar a criação de uma nova senha.
    Ele chama a função do banco de dados e prepara os dados para a resposta.
    """
    if not nome or not tipo:
        return None # Retorna None se os dados forem inválidos

    senha_criada = db.adicionar_senha(nome, tipo)
    
    return {
        "nome": nome,
        "tipo": tipo,
        "senha_gerada": senha_criada['numero_formatado']
    }

def obter_fila_organizada():
    """
    Serviço para buscar as senhas do banco de dados e organizá-las
    na lógica de alternância para exibição no painel.
    """
    comuns = db.get_senhas_por_tipo('C')
    preferenciais = db.get_senhas_por_tipo('P')

    # Lógica de alternância (exatamente como no seu projeto JS original)
    fila_geral = []
    i = 0
    # Usamos o maior comprimento entre as duas listas como limite
    limite = max(len(comuns), len(preferenciais))
    
    while i < limite:
        # Adiciona uma senha preferencial, se ainda houver
        if i < len(preferenciais):
            # dict() converte o objeto sqlite3.Row para um dicionário padrão
            fila_geral.append(dict(preferenciais[i]))
        
        # Adiciona uma senha comum, se ainda houver
        if i < len(comuns):
            fila_geral.append(dict(comuns[i]))
        i += 1
    
    return fila_geral