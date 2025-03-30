from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = -1992910974424714295
NOME_TABELA = "tr_excesso_velocidade_40km_2"

def importar_tr_excesso_velocidade_40km_2():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Excesso de Velocidade 40km 2")
