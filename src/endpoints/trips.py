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

def buscar_trips(token, since_token, tentativas=3, espera=5):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}/api/trips/groups/createdsince/organisation/{ORGANISATION_ID}/sincetoken/{since_token}/quantity/{QUANTITY}?includeSubTrips=true"


    for tentativa in range(1, tentativas + 1):
        try:
            print(f"🔄 Buscando trips (tentativa {tentativa})...")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"⚠️ Erro na requisição: {err}")
            if response.status_code == 429 and tentativa < tentativas:
                print(f"⏳ Aguardando {espera}s para nova tentativa...")
                time.sleep(espera)
            else:
                raise

def importar_trips():
    since_token = gerar_since_token()
    token = autenticar()
    resposta = buscar_trips(token, since_token)
    print("🔍 Resposta recebida da API:")
    print(resposta)

    if isinstance(resposta, dict) and "Trips" in resposta:
        trips = resposta["Trips"]
    else:
        trips = resposta

    if not trips:
        print("📭 Nenhuma trip encontrada.")
        return


    if not trips:
        print("📭 Nenhuma trip encontrada.")
        return

    print(f"📦 Total de trips recebidas: {len(trips)}")
    conn = conectar_banco()
    cursor = conn.cursor()

    inseridas = 0
    for trip in trips:
        if not trip.get("TripId"):
            continue

        sql = """
            INSERT INTO trips (
                TripId, AssetId, DriverId, TripStart, TripEnd, Notes,
                EngineSeconds, FirstDepart, LastHalt, DrivingTime, StandingTime, Duration,
                DistanceKilometers, StartOdometerKilometers, EndOdometerKilometers,
                StartEngineSeconds, EndEngineSeconds, PulseValue, FuelUsedLitres,
                MaxSpeedKilometersPerHour, MaxAccelerationKilometersPerHourPerSecond,
                MaxDecelerationKilometersPerHourPerSecond, MaxRpm
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                TripStart=VALUES(TripStart),
                TripEnd=VALUES(TripEnd),
                Notes=VALUES(Notes),
                EngineSeconds=VALUES(EngineSeconds),
                FirstDepart=VALUES(FirstDepart),
                LastHalt=VALUES(LastHalt),
                DrivingTime=VALUES(DrivingTime),
                StandingTime=VALUES(StandingTime),
                Duration=VALUES(Duration),
                DistanceKilometers=VALUES(DistanceKilometers),
                StartOdometerKilometers=VALUES(StartOdometerKilometers),
                EndOdometerKilometers=VALUES(EndOdometerKilometers),
                StartEngineSeconds=VALUES(StartEngineSeconds),
                EndEngineSeconds=VALUES(EndEngineSeconds),
                PulseValue=VALUES(PulseValue),
                FuelUsedLitres=VALUES(FuelUsedLitres),
                MaxSpeedKilometersPerHour=VALUES(MaxSpeedKilometersPerHour),
                MaxAccelerationKilometersPerHourPerSecond=VALUES(MaxAccelerationKilometersPerHourPerSecond),
                MaxDecelerationKilometersPerHourPerSecond=VALUES(MaxDecelerationKilometersPerHourPerSecond),
                MaxRpm=VALUES(MaxRpm)
        """

        dados = (
            trip.get("TripId"),
            trip.get("AssetId"),
            trip.get("DriverId"),
            parse_date(trip.get("TripStart")),
            parse_date(trip.get("TripEnd")),
            trip.get("Notes"),
            trip.get("EngineSeconds"),
            parse_date(trip.get("FirstDepart")),
            parse_date(trip.get("LastHalt")),
            trip.get("DrivingTime"),
            trip.get("StandingTime"),
            trip.get("Duration"),
            trip.get("DistanceKilometers"),
            trip.get("StartOdometerKilometers"),
            trip.get("EndOdometerKilometers"),
            trip.get("StartEngineSeconds"),
            trip.get("EndEngineSeconds"),
            trip.get("PulseValue"),
            trip.get("FuelUsedLitres"),
            trip.get("MaxSpeedKilometersPerHour"),
            trip.get("MaxAccelerationKilometersPerHourPerSecond"),
            trip.get("MaxDecelerationKilometersPerHourPerSecond"),
            trip.get("MaxRpm")
        )

        cursor.execute(sql, dados)
        inseridas += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {inseridas} trips inseridas/atualizadas com sucesso.")
