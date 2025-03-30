from eventos.importador_base import importar_eventos_por_tipo

EVENT_TYPE_ID = 2164520525956490666
NOME_TABELA = "tr_excesso_rpm_parado"

def importar_tr_excesso_rpm_parado():
    importar_eventos_por_tipo(EVENT_TYPE_ID, NOME_TABELA, "Excesso RPM Parado")
