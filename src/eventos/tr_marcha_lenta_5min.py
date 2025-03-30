from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = -154632669554799975
NOME_TABELA = "tr_marcha_lenta_5min"

def importar_tr_marcha_lenta_5min():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Marcha Lenta 5min")
