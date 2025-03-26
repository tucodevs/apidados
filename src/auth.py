import requests
import os
from dotenv import load_dotenv

load_dotenv()

AUTH_URL = "https://identity.us.mixtelematics.com/core/connect/token"
CLIENT_ID = os.getenv("MIX_CLIENT_ID")
CLIENT_SECRET = os.getenv("MIX_CLIENT_SECRET")
USERNAME = os.getenv("MIX_USERNAME")
PASSWORD = os.getenv("MIX_PASSWORD")
SCOPE = "offline_access MiX.Integrate"

def autenticar():
    data = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": USERNAME,
        "password": PASSWORD,
        "scope": SCOPE
    }
    response = requests.post(AUTH_URL, data=data)
    response.raise_for_status()
    return response.json()["access_token"]
