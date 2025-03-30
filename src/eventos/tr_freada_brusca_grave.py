from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = -1150311268842644462
NOME_TABELA = "tr_freada_brusca_grave"

def importar_tr_freada_brusca_grave():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Freada Brusca Grave")
