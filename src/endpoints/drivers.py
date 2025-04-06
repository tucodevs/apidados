import os
import requests
from core.auth import autenticar
from core.db import conectar_banco
from dotenv import load_dotenv

load_dotenv()

def importar_drivers():
    token = autenticar()
    organisation_id = os.getenv("MIX_ORGANISATION_ID")

    if not organisation_id:
        print("⚠️ ORGANISATION_ID não definido no .env")
        return

    url = f"{os.getenv('MIX_API_URL')}/api/drivers/organisation/{organisation_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erro ao buscar drivers: {response.status_code} - {response.text}")
        return

    drivers = response.json()
    if not isinstance(drivers, list):
        print("Resposta da API não está em formato de lista.")
        return

    conn = conectar_banco()
    cursor = conn.cursor()

    for driver in drivers:
        cursor.execute("""
            INSERT INTO drivers (
                DriverId, OrganisationId, Name, Description, SiteId, SiteName,
                DriverLicenceNumber, DriverLicenceState, DriverLicenceExpiry,
                DriverIdentification, IsActive
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                OrganisationId=VALUES(OrganisationId),
                Name=VALUES(Name),
                Description=VALUES(Description),
                SiteId=VALUES(SiteId),
                SiteName=VALUES(SiteName),
                DriverLicenceNumber=VALUES(DriverLicenceNumber),
                DriverLicenceState=VALUES(DriverLicenceState),
                DriverLicenceExpiry=VALUES(DriverLicenceExpiry),
                DriverIdentification=VALUES(DriverIdentification),
                IsActive=VALUES(IsActive)
        """, (
            driver.get("DriverId"),
            driver.get("OrganisationId"),
            driver.get("Name"),
            driver.get("Description"),
            driver.get("SiteId"),
            driver.get("SiteName"),
            driver.get("DriverLicenceNumber"),
            driver.get("DriverLicenceState"),
            driver.get("DriverLicenceExpiry"),
            driver.get("DriverIdentification"),
            driver.get("IsActive"),
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {len(drivers)} drivers importados/atualizados com sucesso.")
