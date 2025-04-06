import os
import requests
from datetime import datetime
from core.auth import autenticar
from core.db import conectar_banco
from dotenv import load_dotenv

load_dotenv()

def importar_assets():
    token = autenticar()
    group_id = os.getenv("MIX_ORGANISATION_ID")
    base_url = os.getenv("MIX_API_URL")

    if not group_id or not base_url:
        print("⚠️ MIX_API_URL ou MIX_ORGANISATION_ID não definidos no .env")
        return

    url = f"{base_url}/api/assets/group/{group_id}"
    print("📡 URL requisitada:", url)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Erro ao buscar assets: {response.status_code} - {response.text}")
        return

    assets = response.json()
    if not isinstance(assets, list):
        print("⚠️ Resposta da API não está em formato de lista.")
        return

    conn = conectar_banco()
    cursor = conn.cursor()

    for asset in assets:
        # Convertendo CreatedDate de ISO para DATETIME do MySQL
        created_date_raw = asset.get("CreatedDate")
        created_date = None
        if created_date_raw:
            try:
                created_date = datetime.strptime(created_date_raw, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                print(f"⚠️ Formato inválido de CreatedDate: {created_date_raw}")

        cursor.execute("""
            INSERT INTO assets (
                AssetId, AssetTypeId, Description, IsConnectedTrailer, RegistrationNumber,
                SiteId, FuelType, FuelTankCapacity, TargetFuelConsumption, TargetFuelConsumptionUnits,
                TargetHourlyFuelConsumption, TargetHourlyFuelConsumptionUnits, FleetNumber,
                WltpMaxRangeKm, BatteryCapacitykWh, UsableBatteryCapacitykWh, Make, Model, Year,
                VinNumber, SerialNumber, AempEquipmentId, EngineNumber, DefaultDriverId, FmVehicleId,
                AdditionalMobileDevice, Notes, Icon, IconColour, Colour, AssetImage, IsDefaultImage,
                AssetImageUrl, UserState, CreatedBy, CreatedDate, Odometer, EngineHours, Country
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                Description=VALUES(Description),
                IsConnectedTrailer=VALUES(IsConnectedTrailer),
                RegistrationNumber=VALUES(RegistrationNumber),
                SiteId=VALUES(SiteId),
                FuelType=VALUES(FuelType),
                FuelTankCapacity=VALUES(FuelTankCapacity),
                TargetFuelConsumption=VALUES(TargetFuelConsumption),
                TargetFuelConsumptionUnits=VALUES(TargetFuelConsumptionUnits),
                TargetHourlyFuelConsumption=VALUES(TargetHourlyFuelConsumption),
                TargetHourlyFuelConsumptionUnits=VALUES(TargetHourlyFuelConsumptionUnits),
                FleetNumber=VALUES(FleetNumber),
                WltpMaxRangeKm=VALUES(WltpMaxRangeKm),
                BatteryCapacitykWh=VALUES(BatteryCapacitykWh),
                UsableBatteryCapacitykWh=VALUES(UsableBatteryCapacitykWh),
                Make=VALUES(Make),
                Model=VALUES(Model),
                Year=VALUES(Year),
                VinNumber=VALUES(VinNumber),
                SerialNumber=VALUES(SerialNumber),
                AempEquipmentId=VALUES(AempEquipmentId),
                EngineNumber=VALUES(EngineNumber),
                DefaultDriverId=VALUES(DefaultDriverId),
                FmVehicleId=VALUES(FmVehicleId),
                AdditionalMobileDevice=VALUES(AdditionalMobileDevice),
                Notes=VALUES(Notes),
                Icon=VALUES(Icon),
                IconColour=VALUES(IconColour),
                Colour=VALUES(Colour),
                AssetImage=VALUES(AssetImage),
                IsDefaultImage=VALUES(IsDefaultImage),
                AssetImageUrl=VALUES(AssetImageUrl),
                UserState=VALUES(UserState),
                CreatedBy=VALUES(CreatedBy),
                CreatedDate=VALUES(CreatedDate),
                Odometer=VALUES(Odometer),
                EngineHours=VALUES(EngineHours),
                Country=VALUES(Country)
        """, (
            asset.get("AssetId"),
            asset.get("AssetTypeId"),
            asset.get("Description"),
            asset.get("IsConnectedTrailer"),
            asset.get("RegistrationNumber"),
            asset.get("SiteId"),
            asset.get("FuelType"),
            asset.get("FuelTankCapacity"),
            asset.get("TargetFuelConsumption"),
            asset.get("TargetFuelConsumptionUnits"),
            asset.get("TargetHourlyFuelConsumption"),
            asset.get("TargetHourlyFuelConsumptionUnits"),
            asset.get("FleetNumber"),
            asset.get("WltpMaxRangeKm"),
            asset.get("BatteryCapacitykWh"),
            asset.get("UsableBatteryCapacitykWh"),
            asset.get("Make"),
            asset.get("Model"),
            asset.get("Year"),
            asset.get("VinNumber"),
            asset.get("SerialNumber"),
            asset.get("AempEquipmentId"),
            asset.get("EngineNumber"),
            asset.get("DefaultDriverId"),
            asset.get("FmVehicleId"),
            asset.get("AdditionalMobileDevice"),
            asset.get("Notes"),
            asset.get("Icon"),
            asset.get("IconColour"),
            asset.get("Colour"),
            asset.get("AssetImage"),
            asset.get("IsDefaultImage"),
            asset.get("AssetImageUrl"),
            asset.get("UserState"),
            asset.get("CreatedBy"),
            created_date,
            asset.get("Odometer"),
            asset.get("EngineHours"),
            asset.get("Country")
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {len(assets)} assets importados/atualizados com sucesso.")
