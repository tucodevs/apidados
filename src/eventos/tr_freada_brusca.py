from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = 337658916843834225
NOME_TABELA = "tr_freada_brusca"

def importar_tr_freada_brusca():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Freada Brusca")
