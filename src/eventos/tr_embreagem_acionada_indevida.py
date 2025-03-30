from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = -1988381093544824498
NOME_TABELA = "tr_embreagem_acionada_indevida"

def importar_tr_embreagem_acionada_indevida():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Embreagem Acionada Indevidamente")
