import os
from dados_loader import gerar_contexto_geral

def atualizar_contexto_local():
    """Gera o contexto e salva em um arquivo local."""
    contexto = gerar_contexto_geral()

    os.makedirs("dados", exist_ok=True)  

    with open("dados/contexto_atualizado.txt", "w", encoding="utf-8") as f:
        f.write(contexto)

    print("✅ Contexto atualizado e salvo em 'dados/contexto_atualizado.txt'.")

if __name__ == "__main__":
    print("🚀 Atualizando contexto...")
    atualizar_contexto_local()
    print("🎯 Atualização concluída!")
