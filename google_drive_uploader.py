from google.oauth2 import service_account 
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
import os

SERVICE_ACCOUNT_FILE = 'credentials/google_drive_credentials.json'

FOLDER_ID = os.getenv("FOLDER_ID")

def upload_transcricao(transcricao_texto, titulo_documento):

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
    )

    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)

    doc_metadata = {
        'name': titulo_documento,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [FOLDER_ID]
    }
    file = drive_service.files().create(body=doc_metadata, fields='id').execute()
    doc_id = file.get('id')

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

    drive_service.permissions().create(
        fileId=doc_id,
        body={'type': 'anyone', 'role': 'reader'},
    ).execute()

    file = drive_service.files().get(fileId=doc_id, fields='webViewLink').execute()
    return file['webViewLink']
