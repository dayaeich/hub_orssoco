import re
import requests
from hub_notion import buscar_paginas, criar_pagina_nova
from openrouter_client import gerar_analise
from assembly_client import transcrever_audio
from config import NOTION_TOKEN, PROMPTS
from notion_client import Client
from google_drive_uploader import upload_transcricao

# Conectar no Notion
notion = Client(auth=NOTION_TOKEN)

def extrair_links(texto):
    padrao = r'https?://[^\s)]+' 
    return re.findall(padrao, texto)

def corrigir_link_drive(link):
    if "drive.google.com/file/d/" in link:
        try:
            id_arquivo = link.split("/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?export=download&id={id_arquivo}"
        except IndexError:
            return link
    elif "docs.google.com/document/d/" in link:
        try:
            id_arquivo = link.split("/d/")[1].split("/")[0]
            return f"https://docs.google.com/document/d/{id_arquivo}/export?format=txt"
        except IndexError:
            return link
    else:
        return link

def buscar_prompt_automatico(nome_transcricao):
    tipo = nome_transcricao.replace("Transcrição - ", "")
    return f"Analise profundamente esta transcrição de {tipo} e extraia insights importantes, padrões de comportamento e pontos críticos mencionados."

def diagnosticar_banco():
    print("Iniciando diagnóstico do Notion...\n")
    paginas = buscar_paginas()

    if not paginas:
        print("Nenhuma página encontrada no Notion.")
        return

    for pagina in paginas:
        page_id = pagina.get("id")
        propriedades = pagina.get("properties", {})
        nome_projeto = propriedades.get('Nome do Cliente', {}).get('title', [{}])[0].get('plain_text', 'Sem Nome')

        print(f"\nProjeto: {nome_projeto} (ID: {page_id})")

        for nome_campo, valor_campo in propriedades.items():
            print(f"Campo: {nome_campo}")
            if "url" in valor_campo and valor_campo["url"]:
                print(f"   - URL detectada: {valor_campo['url']}")
            if "rich_text" in valor_campo and valor_campo["rich_text"]:
                texto = valor_campo["rich_text"][0]["plain_text"]
                print(f"   - Texto detectado: {texto[:100]}...")
            if "title" in valor_campo and valor_campo["title"]:
                titulo = valor_campo["title"][0]["plain_text"]
                print(f"   - Título detectado: {titulo}")

def processar_projetos():
    print("Buscando projetos no Notion...")
    paginas = buscar_paginas()

    if not paginas:
        print("Nenhuma página encontrada no Notion.")
        return

    for pagina in paginas:
        page_id = pagina.get("id")
        if not page_id:
            continue

        propriedades = pagina.get("properties", {})
        nome_projeto = propriedades.get('Nome do Cliente', {}).get('title', [{}])[0].get('plain_text', 'Sem Nome')
        print(f"\nProcessando projeto: {nome_projeto}")

        audio_campo = propriedades.get("\u00c1udio - Qualificação", {})
        transcricao_campo = propriedades.get("Transcrição - Qualificação", {})

        precisa_transcrever = False

        if "url" in audio_campo and audio_campo["url"]:
            if not (transcricao_campo.get("url") and transcricao_campo["url"]):
                precisa_transcrever = True

        if precisa_transcrever:
            print("Transcrevendo áudio de qualificação...")
            link_audio = corrigir_link_drive(audio_campo["url"])
            try:
                texto_transcrito = transcrever_audio(link_audio, page_id)
                if texto_transcrito:
                    titulo_documento = f"Transcrição - {nome_projeto} - Qualificação"
                    link_doc = upload_transcricao(texto_transcrito, titulo_documento)
                    notion.pages.update(
                        page_id=page_id,
                        properties={
                            "Transcrição - Qualificação": {
                                "url": link_doc
                            }
                        }
                    )
                    print("Transcrição atualizada com sucesso!")
                else:
                    raise Exception("Sem retorno da transcrição.")
            except Exception as e:
                print(f"Erro ao transcrever áudio: {e}")
                notion.pages.update(
                    page_id=page_id,
                    properties={
                        "Transcrição - Qualificação": {
                            "url": ""
                        }
                    }
                )

        for nome_campo, valor_campo in propriedades.items():
            if not nome_campo.startswith("Transcrição - "):
                continue

            nome_analise = nome_campo.replace("Transcrição - ", "Análise - ")
            propriedade_analise = propriedades.get(nome_analise)

            analise_ja_existe = False
            if propriedade_analise and propriedade_analise.get("rich_text", []) and propriedade_analise["rich_text"][0]["plain_text"].strip():
                print(f"Análise para {nome_analise} já existe. Pulando geração de análise...")
                analise_ja_existe = True

            textos_para_analisar = []

            if "url" in valor_campo and valor_campo["url"]:
                url_transcricao = corrigir_link_drive(valor_campo["url"])
                try:
                    response = requests.get(url_transcricao)
                    if response.status_code == 200:
                        textos_para_analisar.append(response.text)
                        print(f"Texto baixado do link de URL direto ({nome_analise}).")
                    else:
                        print(f"Não foi possível baixar o link: {url_transcricao}")
                except Exception as e:
                    print(f"Erro ao baixar o link direto: {e}")
            elif "rich_text" in valor_campo and valor_campo["rich_text"]:
                texto = valor_campo["rich_text"][0]["plain_text"]
                links_encontrados = extrair_links(texto)
                if links_encontrados:
                    for link in links_encontrados:
                        url_corrigido = corrigir_link_drive(link)
                        try:
                            response = requests.get(url_corrigido)
                            if response.status_code == 200:
                                textos_para_analisar.append(response.text)
                                print(f"Texto baixado do link extraído ({nome_analise}).")
                            else:
                                print(f"Não foi possível baixar o link: {url_corrigido}")
                        except Exception as e:
                            print(f"Erro ao baixar o link extraído: {e}")
                else:
                    textos_para_analisar.append(texto)

            for i, texto_transcricao in enumerate(textos_para_analisar, start=1):
                if texto_transcricao.strip():
                    if not analise_ja_existe:
                        print(f"Gerando análise para: {nome_analise} (Texto {i})")
                        prompt = PROMPTS.get(nome_campo, buscar_prompt_automatico(nome_campo))
                        nova_analise = gerar_analise(texto_transcricao, prompt)

                        if nova_analise:
                            pedaços = [nova_analise[i:i+2000] for i in range(0, len(nova_analise), 2000)]
                            try:
                                notion.pages.update(
                                    page_id=page_id,
                                    properties={
                                        nome_analise: {
                                            "rich_text": [{"text": {"content": pedaço}} for pedaço in pedaços]
                                        }
                                    }
                                )
                                print(f"Análise adicionada em {nome_analise}.")
                            except Exception as e:
                                print(f"Erro ao atualizar análise: {e}")

                    nome_sentimento = nome_campo.replace("Transcrição - ", "Sentimento - ")
                    propriedade_sentimento = propriedades.get(nome_sentimento)

                    if propriedade_sentimento and propriedade_sentimento.get("rich_text", []) and propriedade_sentimento["rich_text"][0]["plain_text"].strip():
                        print(f"Sentimento para {nome_sentimento} já existe. Pulando...")
                        continue

                    if nome_sentimento in propriedades:
                        print(f"Gerando sentimento para: {nome_sentimento}")

                        prompt_sentimento = PROMPTS.get("Sentimento - padrão")
                        sentimento = gerar_analise(texto_transcricao, prompt_sentimento)

                        if sentimento:
                            pedaços_sentimento = [sentimento[i:i+2000] for i in range(0, len(sentimento), 2000)]
                            try:
                                notion.pages.update(
                                    page_id=page_id,
                                    properties={
                                        nome_sentimento: {
                                            "rich_text": [{"text": {"content": pedaço}} for pedaço in pedaços_sentimento]
                                        }
                                    }
                                )
                                print(f"Sentimento adicionado em {nome_sentimento}.")
                            except Exception as e:
                                print(f"Erro ao atualizar sentimento: {e}")

def main():
    print("Iniciando processamento...\n")
    diagnosticar_banco()
    print("\nIniciando processamento das análises...\n")
    processar_projetos()
    print("\nProcessamento concluído!")

if __name__ == "__main__":
    main()
