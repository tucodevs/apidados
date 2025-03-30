from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = 6474504604434952727
NOME_TABELA = "tr_excesso_velocidade_40km_1"

def importar_tr_excesso_velocidade_40km_1():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Excesso de Velocidade 40km 1")
