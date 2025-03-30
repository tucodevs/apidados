from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = 6314588935029952465
NOME_TABELA = "tr_inercia_aproveitada"

def importar_tr_inercia_aproveitada():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Inércia Aproveitada")
