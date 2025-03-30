from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = 8889515098300962737
NOME_TABELA = "tr_excesso_rotacao"

def importar_tr_excesso_rotacao():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Excesso de Rotação")
