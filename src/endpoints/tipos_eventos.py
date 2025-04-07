import requests
import os
from dotenv import load_dotenv
from core.db import conectar_banco
from core.auth import autenticar

load_dotenv()

BASE_URL = os.getenv("MIX_API_URL", "https://integrate.us.mixtelematics.com")
ORGANISATION_ID = os.getenv("MIX_ORGANISATION_ID", "5264698351645850280")

def buscar_tipos_eventos(token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}/api/libraryevents/organisation/{ORGANISATION_ID}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def inserir_tipos_eventos(cursor, tipo):
    sql = """
        INSERT INTO tipos_eventos (
            EventTypeId, EventType, Description, DisplayUnits, FormatType, ValueName
        ) VALUES (
            %(EventTypeId)s, %(EventType)s, %(Description)s, %(DisplayUnits)s, %(FormatType)s, %(ValueName)s
        )
        ON DUPLICATE KEY UPDATE
            EventType = VALUES(EventType),
            Description = VALUES(Description),
            DisplayUnits = VALUES(DisplayUnits),
            FormatType = VALUES(FormatType),
            ValueName = VALUES(ValueName);
    """
    dados = {
        "EventTypeId": tipo.get("EventTypeId"),
        "EventType": tipo.get("EventType"),
        "Description": tipo.get("Description"),
        "DisplayUnits": tipo.get("DisplayUnits"),
        "FormatType": tipo.get("FormatType"),
        "ValueName": tipo.get("ValueName")
    }
    cursor.execute(sql, dados)

    # Retorna True se a linha foi inserida ou atualizada
    return cursor.rowcount > 0

def importar_tipos_eventos():
    token = autenticar()
    tipos = buscar_tipos_eventos(token)

    if not tipos:
        print("Nenhum tipo de evento encontrado.")
        return

    conn = conectar_banco()
    cursor = conn.cursor()

    atualizados = 0
    for tipo in tipos:
        descricao = tipo.get("Description", "")
        if descricao.strip().startswith("(Tr)"):
            if inserir_tipos_eventos(cursor, tipo):
                atualizados += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{atualizados} tipos de eventos (Tr) atualizados ou inseridos no banco.")
