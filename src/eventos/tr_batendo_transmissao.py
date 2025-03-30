from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = -4465594527070247088
NOME_TABELA = "tr_batendo_transmissao"

def importar_tr_batendo_transmissao():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Batendo Transmissão")
