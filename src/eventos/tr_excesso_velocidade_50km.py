from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = 5511057473630489154
NOME_TABELA = "tr_excesso_velocidade_50km"

def importar_tr_excesso_velocidade_50km():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Excesso de Velocidade 50km")
