from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = -9050647299058098294
NOME_TABELA = "tr_excesso_velocidade_55km_2"

def importar_tr_excesso_velocidade_55km_2():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Excesso de Velocidade 55km 2")
