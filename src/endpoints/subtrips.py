
import os
import requests
import time
from datetime import datetime, timedelta, timezone
from core.auth import autenticar
from core.db import conectar_banco
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("MIX_API_URL")
ORGANISATION_ID = os.getenv("MIX_ORGANISATION_ID")
QUANTITY = "100"

def gerar_since_token(dias_atras=1):
    data = datetime.now(timezone.utc) - timedelta(days=dias_atras)
    return data.strftime('%Y%m%d%H%M%S') + "000"

def parse_date(data_str):
    if not data_str:
        return None
    try:
        return datetime.strptime(data_str.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
    except:
        return None

def importar_subtrips():
    since_token = gerar_since_token()
    token = autenticar()

    url = f"{BASE_URL}/api/trips/groups/createdsince/organisation/{ORGANISATION_ID}/sincetoken/{since_token}/quantity/{QUANTITY}?includeSubTrips=true"
    headers = {"Authorization": f"Bearer {token}"}

    print(f"🔍 Requisitando trips com subtrips...")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Erro ao buscar trips: {response.status_code} - {response.text}")
        return

    trips = response.json()
    if not isinstance(trips, list):
        print("⚠️ Resposta não é uma lista.")
        return

    conn = conectar_banco()
    cursor = conn.cursor()
    inseridas = 0

    for trip in trips:
        trip_id = trip.get("TripId")
        asset_id = trip.get("AssetId")
        driver_id = trip.get("DriverId")
        subtrips = trip.get("SubTrips", [])

        for sub in subtrips:
            start = parse_date(sub.get("SubTripStart"))
            end = parse_date(sub.get("SubTripEnd"))
            start_od = sub.get("StartOdometerKilometres")
            end_od = sub.get("EndOdometerKilometres")
            distance = sub.get("DistanceKilometres")
            fuel = sub.get("FuelUsedLitres")

            # Dados de posição
            start_pos = sub.get("StartPosition", {})
            end_pos = sub.get("EndPosition", {})

            start_lat = start_pos.get("Latitude")
            start_lon = start_pos.get("Longitude")
            end_lat = end_pos.get("Latitude")
            end_lon = end_pos.get("Longitude")

            sql = '''
                INSERT INTO subtrips (
                    TripId, AssetId, DriverId, SubTripStart, SubTripEnd,
                    StartOdometer, EndOdometer, Distance, FuelUsed,
                    StartLatitude, StartLongitude, EndLatitude, EndLongitude
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    SubTripStart=VALUES(SubTripStart),
                    SubTripEnd=VALUES(SubTripEnd),
                    StartOdometer=VALUES(StartOdometer),
                    EndOdometer=VALUES(EndOdometer),
                    Distance=VALUES(Distance),
                    FuelUsed=VALUES(FuelUsed),
                    StartLatitude=VALUES(StartLatitude),
                    StartLongitude=VALUES(StartLongitude),
                    EndLatitude=VALUES(EndLatitude),
                    EndLongitude=VALUES(EndLongitude)
            '''

            dados = (
                trip_id, asset_id, driver_id, start, end,
                start_od, end_od, distance, fuel,
                start_lat, start_lon, end_lat, end_lon
            )

            cursor.execute(sql, dados)
            inseridas += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {inseridas} subtrips inseridas/atualizadas com sucesso.")
