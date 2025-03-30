from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = 908787025131282024
NOME_TABELA = "tr_excesso_velocidade_60km"

def importar_tr_excesso_velocidade_60km():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Excesso de Velocidade 60km")
