from eventos.tr_excesso_rotacao import importar_excesso_rotacao
from tipos_eventos import atualizar_tipos_eventos

def main():
    try:
        print("🔄 Atualizando tipos de eventos...")
        atualizar_tipos_eventos()

        print("📥 Importando eventos de Excesso de Rotação...")
        importar_excesso_rotacao()

    except Exception as e:
        print("❌ Erro durante execução:", e)

if __name__ == "__main__":
    main()
