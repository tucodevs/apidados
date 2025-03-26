import requests
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from config import DB_CONFIG
from auth import autenticar

load_dotenv()

# Constantes da API
BASE_URL = os.getenv("MIX_API_URL", "https://integrate.us.mixtelematics.com")
ORGANISATION_ID = os.getenv("MIX_ORGANISATION_ID", "5264698351645850280")
QUANTITY = "1000"

def gerar_since_token(dias_atras=1):
    data = datetime.now(timezone.utc) - timedelta(days=dias_atras)
    return data.strftime('%Y%m%d%H%M%S') + "000"

def normalizar_data(data_str):
    if not data_str:
        return None
    try:
        return datetime.strptime(data_str.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None

def buscar_eventos(token, since_token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}/api/events/groups/createdsince/organisation/{ORGANISATION_ID}/sincetoken/{since_token}/quantity/{QUANTITY}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def conectar_banco():
    return mysql.connector.connect(**DB_CONFIG)

def event_type_existe(cursor, event_type_id):
    cursor.execute("SELECT 1 FROM tipos_eventos WHERE EventTypeId = %s", (event_type_id,))
    return cursor.fetchone() is not None

def inserir_evento(cursor, evento):
    sql = """
        INSERT INTO eventos (
            AssetId, DriverId, EventId, EventTypeId, EventCategory,
            StartDateTime, StartOdometerKilometres, StartLatitude, StartLongitude,
            StartSpeedKph, StartOdometer, StartTimestamp,
            EndDateTime, EndOdometerKilometres, EndLatitude, EndLongitude,
            EndSpeedKph, EndOdometer, EndTimestamp,
            Value, FuelUsedLitres, ValueType, ValueUnits,
            TotalTimeSeconds, TotalOccurances, SpeedLimit
        ) VALUES (
            %(AssetId)s, %(DriverId)s, %(EventId)s, %(EventTypeId)s, %(EventCategory)s,
            %(StartDateTime)s, %(StartOdometerKilometres)s, %(StartLatitude)s, %(StartLongitude)s,
            %(StartSpeedKph)s, %(StartOdometer)s, %(StartTimestamp)s,
            %(EndDateTime)s, %(EndOdometerKilometres)s, %(EndLatitude)s, %(EndLongitude)s,
            %(EndSpeedKph)s, %(EndOdometer)s, %(EndTimestamp)s,
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
        "StartOdometerKilometres": evento.get("StartOdometerKilometres"),
        "StartLatitude": evento.get("StartPosition", {}).get("Latitude"),
        "StartLongitude": evento.get("StartPosition", {}).get("Longitude"),
        "StartSpeedKph": evento.get("StartPosition", {}).get("SpeedKilometresPerHour"),
        "StartOdometer": evento.get("StartPosition", {}).get("OdometerKilometres"),
        "StartTimestamp": normalizar_data(evento.get("StartPosition", {}).get("Timestamp")),
        "EndDateTime": normalizar_data(evento.get("EndDateTime")),
        "EndOdometerKilometres": evento.get("EndOdometerKilometres"),
        "EndLatitude": evento.get("EndPosition", {}).get("Latitude"),
        "EndLongitude": evento.get("EndPosition", {}).get("Longitude"),
        "EndSpeedKph": evento.get("EndPosition", {}).get("SpeedKilometresPerHour"),
        "EndOdometer": evento.get("EndPosition", {}).get("OdometerKilometres"),
        "EndTimestamp": normalizar_data(evento.get("EndPosition", {}).get("Timestamp")),
        "Value": evento.get("Value"),
        "FuelUsedLitres": evento.get("FuelUsedLitres"),
        "ValueType": evento.get("ValueType"),
        "ValueUnits": evento.get("ValueUnits"),
        "TotalTimeSeconds": evento.get("TotalTimeSeconds"),
        "TotalOccurances": evento.get("TotalOccurances"),
        "SpeedLimit": evento.get("SpeedLimit")
    }

    cursor.execute(sql, dados)

def processar_eventos():
    since_token = gerar_since_token()
    token = autenticar()
    eventos = buscar_eventos(token, since_token)

    if not eventos:
        print("Nenhum evento encontrado.")
        return

    conn = conectar_banco()
    cursor = conn.cursor()

    ignorados = 0
    inseridos = 0

    for evento in eventos:
        event_type_id = evento.get("EventTypeId")
        if not event_type_existe(cursor, event_type_id):
            print(f"Ignorando EventTypeId não mapeado: {event_type_id}")
            ignorados += 1
            continue

        inserir_evento(cursor, evento)
        inseridos += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{inseridos} eventos inseridos com sucesso.")
    print(f"{ignorados} eventos ignorados por EventTypeId não encontrado.")
