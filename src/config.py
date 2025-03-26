import os
from dotenv import load_dotenv

# Carrega o .env na inicialização
load_dotenv()

# Configurações do banco
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

