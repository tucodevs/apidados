
import os
import sys
import shutil
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "viaverde")

PASTA_FINAL = os.path.join("C:\\ViaverdeImportador")
EXE_PRINCIPAL = "main_gui.exe"
CREATE_TABLES_PATH = os.path.join("sql", "create_tables.sql")

def conectar_mariadb(database=None):
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=database
    )

def criar_banco():
    conn = conectar_mariadb()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Banco '{DB_NAME}' criado/verificado.")

def executar_create_tables():
    conn = conectar_mariadb(database=DB_NAME)
    cursor = conn.cursor()
    with open(CREATE_TABLES_PATH, "r", encoding="utf-8") as f:
        comandos = f.read().split(";")
        for comando in comandos:
            if comando.strip():
                try:
                    cursor.execute(comando)
                except Exception as e:
                    print("⚠️ Erro no SQL:", e)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tabelas criadas/verificadas.")

def copiar_arquivos():
    print("📁 Copiando arquivos...")
    base = getattr(sys, '_MEIPASS', os.path.abspath("."))
    os.makedirs(PASTA_FINAL, exist_ok=True)

    for nome in ["main_gui.exe", ".env"]:
        src = os.path.join(base, nome)
        dst = os.path.join(PASTA_FINAL, nome)
        if os.path.exists(src):
            shutil.copy2(src, dst)

    sql_origem = os.path.join(base, "sql")
    sql_destino = os.path.join(PASTA_FINAL, "sql")
    if os.path.exists(sql_origem):
        shutil.copytree(sql_origem, sql_destino, dirs_exist_ok=True)

    print("✅ Arquivos copiados.")

def executar_app():
    exe_path = os.path.join(PASTA_FINAL, EXE_PRINCIPAL)
    print(f"▶️ Iniciando {EXE_PRINCIPAL}...")
    os.startfile(exe_path)

if __name__ == "__main__":
    print("🚀 Iniciando instalador Viaverde")
    try:
        criar_banco()
        executar_create_tables()
        copiar_arquivos()
        executar_app()
        print("✅ Instalação concluída.")
    except Exception as e:
        print("❌ Erro na instalação:", e)
        sys.exit(1)
