from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = -6437542951044419628
NOME_TABELA = "tr_fora_faixa_verde"

def importar_tr_fora_faixa_verde():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Fora da Faixa Verde")
