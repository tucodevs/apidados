import time
import schedule
from importador_lote import importar_eventos_lote

def tarefa():
    print("⏰ Executando importação automática...")
    try:
        importar_eventos_lote()
    except Exception as e:
        print("❌ Erro na importação:", e)

def iniciar_agendador():
    schedule.every(15).minutes.do(tarefa)
    print("🔁 Agendador iniciado. Rodando a cada 15 minutos.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    print("🚀 Iniciando aplicação...")
    tarefa()  # executa a primeira importação logo ao iniciar
    iniciar_agendador()
