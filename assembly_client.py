import requests
import time
from config import ASSEMBLY_API_KEY
from hub_notion import buscar_paginas, atualizar_transcricao_qualificacao

def verificar_audio_ja_transcrito(link_audio):
    """Verifica se o link do áudio já foi transcrito antes no Notion."""
    paginas = buscar_paginas()
    for pagina in paginas:
        propriedades = pagina["properties"]
        transcricao_qualificacao = propriedades.get("Transcrição - Qualificação", {}).get("rich_text", [])
        if transcricao_qualificacao:
            texto_transcricao = transcricao_qualificacao[0].get("plain_text", "")
            if link_audio in texto_transcricao:
                return True
    return False

def transcrever_audio(url_audio, page_id):
    """Envia o link público do áudio para AssemblyAI e retorna o texto transcrito."""
    try:
        if verificar_audio_ja_transcrito(url_audio):
            print("⚠️ O áudio já foi transcrito anteriormente. Ignorando...")
            return None

        endpoint = "https://api.assemblyai.com/v2/transcript"
        headers = {
            "authorization": ASSEMBLY_API_KEY,
            "content-type": "application/json"
        }
        json_data = {
            "audio_url": url_audio,
            "language_code": "pt",
            "auto_chapters": False,
            "iab_categories": False
        }
        response = requests.post(endpoint, headers=headers, json=json_data)
        response.raise_for_status()

        transcript_id = response.json()["id"]
        endpoint_resultado = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

        loading_chars = ["|", "/", "-", "\\"]
        loading_index = 0

        print("⌛ Transcrevendo áudio, aguarde...")

        while True:
            resultado = requests.get(endpoint_resultado, headers=headers)
            resultado.raise_for_status()
            status = resultado.json()["status"]

            if status == "completed":
                print("\n✅ Transcrição concluída!")
                texto_transcrito = resultado.json()["text"]
                
                # Atualiza a transcrição no Notion
                print("📥 Atualizando transcrição no Notion...")
                atualizar_transcricao_qualificacao(page_id=page_id, texto_transcricao=texto_transcrito)
                
                return texto_transcrito
            elif status == "failed":
                erro = resultado.json().get("error", "Sem detalhes fornecidos.")
                print(f"\n❌ Erro na transcrição! Detalhes: {erro}")
                raise Exception(f"Erro na transcrição: {erro}")

            print(loading_chars[loading_index % len(loading_chars)], end="\r")
            loading_index += 1
            time.sleep(2)

    except Exception as e:
        print(f"\n❌ Erro inesperado na transcrição: {str(e)}")
        raise e
