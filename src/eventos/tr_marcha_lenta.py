from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = 2561992611692992861
NOME_TABELA = "tr_marcha_lenta"

def importar_tr_marcha_lenta():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Marcha Lenta")
