from . import database as db

def gerar_nova_senha(nome, tipo):
    """
    Serviço para coordenar a criação de uma nova senha.
    Ele chama a função do banco de dados e prepara os dados para a resposta.
    """
    if not nome or not tipo:
        return None
    senha_criada = db.adicionar_senha(nome, tipo)
    
    return {
        "nome": nome,
        "tipo": tipo,
        "senha_gerada": senha_criada['numero_formatado']
    }

def obter_fila_organizada():
    """
    Calcula a ordem de prioridade estável (2P para 1C) para todas as senhas do dia
    e retorna apenas as que ainda estão a aguardar.
    """
    
    todas_as_senhas = db.get_todas_as_senhas_do_dia()

    todas_preferenciais = [s for s in todas_as_senhas if s['tipo'].startswith('P')]
    todas_comuns = [s for s in todas_as_senhas if not s['tipo'].startswith('P')]

    fila_mestra = []
    idx_p = 0
    idx_c = 0
    PRIORITY_RATIO = 2

    while idx_p < len(todas_preferenciais) or idx_c < len(todas_comuns):

        for _ in range(PRIORITY_RATIO):
            if idx_p < len(todas_preferenciais):
                fila_mestra.append(dict(todas_preferenciais[idx_p]))
                idx_p += 1
        if idx_c < len(todas_comuns):
            fila_mestra.append(dict(todas_comuns[idx_c]))
            idx_c += 1

    fila_final_aguardando = [s for s in fila_mestra if s['status'] == 'aguardando']

    return fila_final_aguardando
