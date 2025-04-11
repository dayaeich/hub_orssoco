from flask import Flask, request
import os
import requests

from config import TELEGRAM_TOKEN, OPENAI_API_KEY, ASSISTANT_ID

app = Flask(__name__)

def enviar_mensagem_telegram(chat_id, mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erro ao enviar mensagem para Telegram: {e}")

def consultar_assistente_openai(pergunta_usuario):
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "assistants=v1",
            "Content-Type": "application/json"
        }

        thread_response = requests.post(
            "https://api.openai.com/v1/threads",
            headers=headers
        )
        thread_response.raise_for_status()
        thread_id = thread_response.json()["id"]

        mensagem_payload = {
            "role": "user",
            "content": pergunta_usuario
        }
        requests.post(
            f"https://api.openai.com/v1/threads/{thread_id}/messages",
            headers=headers,
            json=mensagem_payload
        )

        run_payload = {
            "assistant_id": ASSISTANT_ID
        }
        run_response = requests.post(
            f"https://api.openai.com/v1/threads/{thread_id}/runs",
            headers=headers,
            json=run_payload
        )
        run_response.raise_for_status()
        run_id = run_response.json()["id"]

        status = "queued"
        while status in ["queued", "in_progress"]:
            check_response = requests.get(
                f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}",
                headers=headers
            )
            status = check_response.json()["status"]

        mensagens_response = requests.get(
            f"https://api.openai.com/v1/threads/{thread_id}/messages",
            headers=headers
        )
        mensagens_response.raise_for_status()
        mensagens = mensagens_response.json()["data"]

        for mensagem in mensagens:
            if mensagem["role"] == "assistant":
                return mensagem["content"][0]["text"]["value"]

    except Exception as e:
        print(f"Erro ao consultar Assistente: {e}")
        return "❌ Erro ao consultar o assistente."

@app.route('/', methods=['POST'])
def webhook_telegram():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        texto_usuario = data["message"]["text"]

        resposta = consultar_assistente_openai(texto_usuario)
        enviar_mensagem_telegram(chat_id, resposta)

    return "OK", 200

@app.route('/main', methods=['POST'])
def rodar_main():
    from main import main
    main()
    return "✅ Main executado com sucesso!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
