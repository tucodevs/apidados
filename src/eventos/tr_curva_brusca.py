from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = 3296322604872944138
NOME_TABELA = "tr_curva_brusca"

def importar_tr_curva_brusca():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Curva Brusca")
