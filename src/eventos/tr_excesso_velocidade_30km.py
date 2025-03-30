from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = -6248653914463313400
NOME_TABELA = "tr_excesso_velocidade_30km"

def importar_tr_excesso_velocidade_30km():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Excesso de Velocidade 30km")
