# Hub OrssoCo

Automação inteligente para transcrição, análise e organização de reuniões comerciais.

## Sobre o projeto

O Hub OrssoCo é uma solução desenvolvida para integrar inteligência artificial ao fluxo de operações comerciais, utilizando Python, APIs customizadas, Notion, Google Cloud, OpenRouter e AssemblyAI.

O sistema realiza:
- Transcrição automática de reuniões
- Análise de sentimentos
- Geração de insights estratégicos
- Organização automatizada de informações no Notion

## Tecnologias Utilizadas

- Python
- Make / Integromat
- Notion API
- Google Drive API
- OpenRouter (LLMs)
- AssemblyAI (Transcrição)

## Estrutura do Projeto

```
hub_orssoco/
├── app.py
├── assembly_client.py
├── atualizar_contexto_assistant.py
├── config.py
├── dados_loader.py
├── Dockerfile
├── google_drive_uploader.py
├── hub_notion.py
├── main.py
├── openrouter_client.py
├── server.py
├── requirements.txt
├── .env (não incluído no repositório por segurança)
├── credentials/ (não incluído no repositório por segurança)
└── README.md
```

## Como rodar o projeto

1. Clone este repositório:
   ```bash
   git clone https://github.com/dayaeich/hub_orssoco.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd hub_orssoco
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente no arquivo `.env` local.
5. Execute o projeto:
   ```bash
   python main.py
   ```

> ⚡ **Importante:** As credenciais e chaves de API (OpenRouter, AssemblyAI, Google Drive) devem ser configuradas localmente e não estão disponíveis no repositório por questões de segurança.
