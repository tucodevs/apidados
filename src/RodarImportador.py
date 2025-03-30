import os
import sys
import time
import schedule
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from threading import Thread
from datetime import datetime, timedelta
from dotenv import load_dotenv
import mysql.connector
from db import conectar_banco
from importador_lote import importar_eventos_lote
from auth import autenticar

# Detectar base path (modo frozen para .exe)
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(__file__)

# Carregar .env
load_dotenv(os.path.join(BASE_DIR, ".env"))

proxima_execucao = None
agendador_ativo = False

def criar_banco_e_tabelas():
    DB_NAME = os.getenv("DB_NAME", "viaverde")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "ViaVerdeDB123")
    DB_HOST = os.getenv("DB_HOST", "localhost")

    print("🛠️ Verificando banco de dados...")

    try:
        # Conectar sem banco selecionado
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Criar banco
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✅ Banco '{DB_NAME}' criado/verificado.")

        # (Re)configurar usuário root
        try:
            cursor.execute(f"ALTER USER '{DB_USER}'@'localhost' IDENTIFIED BY '{DB_PASSWORD}'")
            print(f"🔐 Usuário '{DB_USER}' configurado.")
        except:
            print("⚠️ Não foi possível alterar usuário (talvez já esteja configurado).")

        # Conceder permissões
        cursor.execute(f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{DB_USER}'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")

        cursor.close()
        conn.commit()
        conn.close()

    except Exception as e:
        print("❌ Erro ao criar banco ou usuário:", e)
        return

    try:
        # Executar SQL de criação de tabelas
        conn = conectar_banco()
        cursor = conn.cursor()
        caminho_sql = os.path.join(BASE_DIR, "sql", "create_tables.sql")
        with open(caminho_sql, "r", encoding="utf-8") as f:
            comandos = f.read().split(";")
            for cmd in comandos:
                if cmd.strip():
                    try:
                        cursor.execute(cmd)
                    except Exception as err:
                        print("⚠️ Erro ao criar tabela:", err)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Tabelas verificadas/criadas.")
    except Exception as e:
        print("❌ Erro ao executar o SQL de criação:", e)

# GUI e lógica de importação
def atualizar_log(texto):
    log_area.config(state='normal')
    log_area.delete(1.0, 'end')
    log_area.insert('end', texto)
    log_area.config(state='disabled')

def testar_conexao():
    try:
        autenticar()
        messagebox.showinfo("Conexão bem-sucedida", "✅ API autenticada com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"❌ Falha ao autenticar:\n{e}")

def executar_importacao():
    global proxima_execucao
    try:
        resultado = importar_eventos_lote(retornar_log=True)
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log = f"🕒 Última execução: {agora}\n\n"
        total = 0
        for tipo, valores in resultado.items():
            log += f"📥 {tipo}: {valores['inseridos']} inseridos de {valores['recebidos']}\n"
            total += valores['inseridos']
        log += f"\n✅ Total inserido: {total}\n"
        atualizar_log(log)
        proxima_execucao = datetime.now() + timedelta(minutes=15)
    except Exception as e:
        atualizar_log(f"❌ Erro na importação: {e}")

def loop_agendador():
    schedule.every(15).minutes.do(executar_importacao)
    global proxima_execucao
    proxima_execucao = datetime.now() + timedelta(minutes=15)
    while True:
        schedule.run_pending()
        time.sleep(1)

def iniciar_agendador():
    global agendador_ativo
    if agendador_ativo:
        return
    agendador_ativo = True
    Thread(target=loop_agendador, daemon=True).start()
    executar_importacao()
    messagebox.showinfo("Agendador Ativado", "✅ Importação automática ativada a cada 15 minutos.")

def atualizar_timer():
    if proxima_execucao:
        restante = proxima_execucao - datetime.now()
        if restante.total_seconds() > 0:
            minutos, segundos = divmod(int(restante.total_seconds()), 60)
            timer_var.set(f"⏳ Próxima importação em: {minutos:02d}:{segundos:02d}")
        else:
            timer_var.set("⏳ Executando agora...")
    else:
        timer_var.set("⏳ Aguardando ativação...")

    app.after(1000, atualizar_timer)

# Interface
app = tk.Tk()
app.title("Importador Viaverde")
app.geometry("700x500")
app.resizable(False, False)

frame = ttk.Frame(app, padding=20)
frame.pack(fill="both", expand=True)

title = ttk.Label(frame, text="Importador Viaverde", font=("Segoe UI", 16, "bold"))
title.pack(pady=(0, 20))

btn_conectar = ttk.Button(frame, text="🔌 Testar Conexão com API", command=testar_conexao, width=40)
btn_conectar.pack(pady=10)

btn_ativar = ttk.Button(frame, text="▶️ Ativar Importação Automática", command=iniciar_agendador, width=40)
btn_ativar.pack(pady=10)

timer_var = tk.StringVar()
timer_label = ttk.Label(frame, textvariable=timer_var, font=("Segoe UI", 11, "italic"), foreground="#555")
timer_label.pack(pady=10)

log_box = ttk.LabelFrame(frame, text="Log da Última Importação", padding=10)
log_box.pack(fill="both", expand=True, pady=15)

log_area = ScrolledText(log_box, height=12, font=("Consolas", 10), state='disabled', wrap='word')
log_area.pack(fill="both", expand=True)

# Rodar verificação de banco e interface
criar_banco_e_tabelas()
atualizar_timer()
app.mainloop()
