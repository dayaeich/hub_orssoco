import os
import PyPDF2
from notion_client import Client
from config import NOTION_TOKEN, NOTION_DATABASE_ID

notion = Client(auth=NOTION_TOKEN)

def buscar_paginas_notion():
    """Busca todas as páginas do Notion."""
    try:
        query = notion.databases.query(database_id=NOTION_DATABASE_ID)
        return query.get('results', [])
    except Exception as e:
        print(f"❌ Erro ao buscar páginas no Notion: {e}")
        return []

def ler_texto_pdfs(pasta='dados/pdfs'):
    """Lê e extrai texto de todos os PDFs na pasta."""
    textos = []
    if not os.path.exists(pasta):
        print(f"⚠️ Pasta '{pasta}' não encontrada.")
        return textos
    
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith('.pdf'):
            caminho = os.path.join(pasta, nome_arquivo)
            try:
                with open(caminho, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    texto = ''
                    for pagina in reader.pages:
                        texto += pagina.extract_text() or ''
                    textos.append(texto.strip())
            except Exception as e:
                print(f"❌ Erro lendo PDF '{nome_arquivo}': {e}")
    return textos

def gerar_contexto_geral():
    """Gera o contexto geral com dados do Notion + PDFs."""
    contexto = []

    paginas = buscar_paginas_notion()
    for pagina in paginas:
        propriedades = pagina.get('properties', {})
        nome_cliente = propriedades.get('Nome do Cliente', {}).get('title', [{}])[0].get('plain_text', 'Cliente Desconhecido')

        contexto.append(f"Cliente: {nome_cliente}")

        for nome_campo, valor_campo in propriedades.items():
            if "rich_text" in valor_campo and valor_campo["rich_text"]:
                texto = valor_campo["rich_text"][0]["plain_text"]
                if texto:
                    contexto.append(f"{nome_campo}: {texto}")
            if "url" in valor_campo and valor_campo["url"]:
                contexto.append(f"{nome_campo} (link): {valor_campo['url']}")

        contexto.append("")  
        
    textos_pdfs = ler_texto_pdfs()
    for i, texto_pdf in enumerate(textos_pdfs, start=1):
        contexto.append(f"Documento PDF {i}:\n{texto_pdf}")

    return "\n".join(contexto)
