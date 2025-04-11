from notion_client import Client
from config import NOTION_TOKEN, NOTION_DATABASE_ID

notion = Client(auth=NOTION_TOKEN)

def buscar_paginas():
    """Busca todas as páginas do banco de dados."""
    try:
        response = notion.databases.query(
            database_id=NOTION_DATABASE_ID
        )
        return response.get("results", [])
    except Exception as e:
        print(f"Erro ao buscar páginas no Notion: {e}")
        return []

def criar_pagina_nova(dados_transcricao):
    """Cria uma nova página no banco de dados com os dados da transcrição."""
    try:
        transcricao = dados_transcricao['transcricao']
        pedaços = [transcricao[i:i+2000] for i in range(0, len(transcricao), 2000)]

        response = notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties={
                "Nome do Projeto": {
                    "title": [{"text": {"content": dados_transcricao['nome_projeto']}}]
                },
                "Áudio - Qualificação": {
                    "url": dados_transcricao['link_audio']
                },
                "Transcrição - Qualificação": {
                    "rich_text": [{"text": {"content": pedaço}} for pedaço in pedaços]
                }
            }
        )
        return response
    except Exception as e:
        print(f"Erro ao criar nova página no Notion: {e}")
        return None

def atualizar_transcricao_qualificacao(page_id, texto_transcricao, campo_transcricao="Transcrição - Qualificação"):
    """Atualiza o campo de transcrição específico na página do Notion."""
    try:
        pedaços = [texto_transcricao[i:i+2000] for i in range(0, len(texto_transcricao), 2000)]

        notion.pages.update(
            page_id=page_id,
            properties={
                campo_transcricao: {
                    "rich_text": [{"text": {"content": pedaço}} for pedaço in pedaços]
                }
            }
        )
        print(f"✅ Campo '{campo_transcricao}' atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar campo '{campo_transcricao}': {e}")

def atualizar_analises(page_id, nova_analise, campo_analise="Análises"):
    """Adiciona ou atualiza o campo de análises na página do Notion."""
    try:
        pagina = notion.pages.retrieve(page_id=page_id)
        analises_atuais = ""

        if campo_analise in pagina["properties"]:
            rich_text = pagina["properties"][campo_analise].get("rich_text", [])
            if rich_text:
                analises_atuais = rich_text[0]["plain_text"]

        texto_final = f"{analises_atuais}\n\n{nova_analise}" if analises_atuais else nova_analise
        pedaços = [texto_final[i:i+2000] for i in range(0, len(texto_final), 2000)]

        notion.pages.update(
            page_id=page_id,
            properties={
                campo_analise: {
                    "rich_text": [{"text": {"content": pedaço}} for pedaço in pedaços]
                }
            }
        )
        print(f"✅ Análise atualizada no campo '{campo_analise}'!")
    except Exception as e:
        print(f"Erro ao atualizar análise em '{campo_analise}': {e}")
