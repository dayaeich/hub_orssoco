import requests
from config import OPENROUTER_API_KEY

def gerar_analise(texto_transcricao, prompt_personalizado):
    """Envia o texto + prompt para o modelo via OpenRouter e recebe a análise."""

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Monta o prompt final: prompt personalizado + texto da transcrição
    prompt_final = f"{prompt_personalizado}\n\nTexto da Transcrição:\n{texto_transcricao}"

    data = {
        "model": "anthropic/claude-3-sonnet-20240229",
        "messages": [
            {
                "role": "user",
                "content": prompt_final
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        resposta = response.json()

        if "choices" in resposta and resposta["choices"]:
            return resposta["choices"][0]["message"]["content"]
        else:
            print("⚠️ Resposta inesperada: 'choices' vazio ou ausente.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição para OpenRouter: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao gerar análise: {e}")
        return None
