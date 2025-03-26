import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from db import conectar_banco
from auth import autenticar

load_dotenv()

BASE_URL = os.getenv("MIX_API_URL", "https://integrate.us.mixtelematics.com")
ORGANISATION_ID = os.getenv("MIX_ORGANISATION_ID", "5264698351645850280")
QUANTITY = "1000"
EVENT_TYPE_ROTACAO = -9050647299058098294

def gerar_since_token(dias_atras=1):
    data = datetime.now(timezone.utc) - timedelta(days=dias_atras)
    return data.strftime('%Y%m%d%H%M%S') + "000"

def normalizar_data(data_str):
    if not data_str:
        return None
    try:
        return datetime.strptime(data_str.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
    except:
        return None

def buscar_eventos(token, since_token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}/api/events/groups/createdsince/organisation/{ORGANISATION_ID}/sincetoken/{since_token}/quantity/{QUANTITY}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def inserir_evento(cursor, evento):
    sql = """
        INSERT INTO tr_excesso_rotacao (
            AssetId, DriverId, EventId, EventTypeId, EventCategory,
            StartDateTime, StartLatitude, StartLongitude, StartSpeedKph, StartOdometer,
            EndDateTime, EndLatitude, EndLongitude, EndSpeedKph, EndOdometer,
            Value, FuelUsedLitres, ValueType, ValueUnits,
            TotalTimeSeconds, TotalOccurances, SpeedLimit
        ) VALUES (
            %(AssetId)s, %(DriverId)s, %(EventId)s, %(EventTypeId)s, %(EventCategory)s,
            %(StartDateTime)s, %(StartLatitude)s, %(StartLongitude)s, %(StartSpeedKph)s, %(StartOdometer)s,
            %(EndDateTime)s, %(EndLatitude)s, %(EndLongitude)s, %(EndSpeedKph)s, %(EndOdometer)s,
            %(Value)s, %(FuelUsedLitres)s, %(ValueType)s, %(ValueUnits)s,
            %(TotalTimeSeconds)s, %(TotalOccurances)s, %(SpeedLimit)s
        )
    """

    dados = {
        "AssetId": evento.get("AssetId"),
        "DriverId": evento.get("DriverId"),
        "EventId": evento.get("EventId"),
        "EventTypeId": evento.get("EventTypeId"),
        "EventCategory": evento.get("EventCategory"),
        "StartDateTime": normalizar_data(evento.get("StartDateTime")),
        "StartLatitude": evento.get("StartPosition", {}).get("Latitude"),
        "StartLongitude": evento.get("StartPosition", {}).get("Longitude"),
        "StartSpeedKph": evento.get("StartPosition", {}).get("SpeedKilometresPerHour"),
        "StartOdometer": evento.get("StartPosition", {}).get("OdometerKilometres"),
        "EndDateTime": normalizar_data(evento.get("EndDateTime")),
        "EndLatitude": evento.get("EndPosition", {}).get("Latitude"),
        "EndLongitude": evento.get("EndPosition", {}).get("Longitude"),
        "EndSpeedKph": evento.get("EndPosition", {}).get("SpeedKilometresPerHour"),
        "EndOdometer": evento.get("EndPosition", {}).get("OdometerKilometres"),
        "Value": evento.get("Value"),
        "FuelUsedLitres": evento.get("FuelUsedLitres"),
        "ValueType": evento.get("ValueType"),
        "ValueUnits": evento.get("ValueUnits"),
        "TotalTimeSeconds": evento.get("TotalTimeSeconds"),
        "TotalOccurances": evento.get("TotalOccurances"),
        "SpeedLimit": evento.get("SpeedLimit")
    }

    cursor.execute(sql, dados)

def importar_excesso_rotacao():
    since_token = gerar_since_token()
    token = autenticar()
    eventos = buscar_eventos(token, since_token)

    if not eventos:
        print("Nenhum evento encontrado.")
        return

    eventos_filtrados = [e for e in eventos if e.get("EventTypeId") == EVENT_TYPE_ROTACAO]

    if not eventos_filtrados:
        print("Nenhum evento de Excesso de Rotação encontrado.")
        return

    conn = conectar_banco()
    cursor = conn.cursor()

    for evento in eventos_filtrados:
        inserir_evento(cursor, evento)

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(eventos_filtrados)} eventos de Excesso de Rotação inseridos com sucesso.")
