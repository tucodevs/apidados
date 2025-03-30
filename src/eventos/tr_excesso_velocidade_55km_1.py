from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = 6580201539568389304
NOME_TABELA = "tr_excesso_velocidade_55km_1"

def importar_tr_excesso_velocidade_55km_1():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Excesso de Velocidade 55km 1")
