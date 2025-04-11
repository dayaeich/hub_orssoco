from google.oauth2 import service_account 
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

# Caminho para sua chave JSON (corrigido para ser relativo e portátil)
SERVICE_ACCOUNT_FILE = 'credentials/google_drive_credentials.json'

# ID da pasta onde vai salvar
FOLDER_ID = '1tgaLWMlH7NosDytIGI7jrPo3hs8JP3f9'

def upload_transcricao(transcricao_texto, titulo_documento):
    # Autenticação
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
    )

    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)

    # Cria o arquivo Google Docs
    doc_metadata = {
        'name': titulo_documento,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [FOLDER_ID]
    }
    file = drive_service.files().create(body=doc_metadata, fields='id').execute()
    doc_id = file.get('id')

    # Insere o texto
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={
            'requests': [
                {
                    'insertText': {
                        'location': {
                            'index': 1,
                        },
                        'text': transcricao_texto
                    }
                }
            ]
        }
    ).execute()

    # Torna o documento visível para quem tem o link
    drive_service.permissions().create(
        fileId=doc_id,
        body={'type': 'anyone', 'role': 'reader'},
    ).execute()

    # Pega o link
    file = drive_service.files().get(fileId=doc_id, fields='webViewLink').execute()
    return file['webViewLink']
