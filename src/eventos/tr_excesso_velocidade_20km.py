from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = 74735825877637374
NOME_TABELA = "tr_excesso_velocidade_20km"

def importar_tr_excesso_velocidade_20km():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Excesso de Velocidade 20km")
