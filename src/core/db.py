import mysql.connector
from core.config import DB_CONFIG

def conectar_banco():
    return mysql.connector.connect(**DB_CONFIG)
