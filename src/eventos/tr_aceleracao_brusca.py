from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = -614457561876096876
NOME_TABELA = "tr_aceleracao_brusca"

def importar_tr_aceleracao_brusca():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Aceleração Brusca")
