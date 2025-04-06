
import os
import sys
from core.auth import autenticar
from core.importador_lote import importar_eventos_lote
from endpoints.drivers import importar_drivers
from endpoints.assets import importar_assets
from endpoints.trips import importar_trips
from endpoints.subtrips import importar_subtrips
from dotenv import load_dotenv

# Detectar base path (modo frozen para .exe)
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(__file__)

# Carregar .env corretamente
load_dotenv(os.path.join(BASE_DIR, ".env"))

if __name__ == "__main__":
    print("🔐 Autenticando na API...")
    autenticar()
    
    print("\n🚚 Importando eventos TR...")
    importar_eventos_lote()

    print("\n👨‍✈️ Importando motoristas...")
    importar_drivers()

    print("\n🚗 Importando ativos (assets)...")
    importar_assets()

    print("\n🧭 Importando viagens (trips)...")
    importar_trips()

    print("\n🧩 Importando subtrips...")
    importar_subtrips()

    print("\n✅ Importação completa.")
