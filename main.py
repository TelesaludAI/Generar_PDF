from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from docx import Document
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import aiofiles


from fastapi import FastAPI, UploadFile, Form
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
import pickle
import io
import json
import os

app = FastAPI()

# === CONFIGURACIÓN ===
FOLDER_ID = "1E4brfQPnwurTivj8mjpdAtc_ByprLbNL"    # ID de la carpeta de destino en Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    # Decodifica credentials.json y token.pkl desde variables de entorno
    credentials_b64 = os.getenv("GOOGLE_CREDENTIALS_BASE64")
    token_b64 = os.getenv("GOOGLE_TOKEN_BASE64")

    if not credentials_b64 or not token_b64:
        raise Exception("⚠️ Variables de entorno no configuradas correctamente.")

    # Reconstruye los archivos en memoria
    credentials_data = json.loads(base64.b64decode(credentials_b64).decode('utf-8'))
    creds = pickle.loads(base64.b64decode(token_b64))

    # Refresca el token si está vencido
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("⚠️ Token inválido o caducado. Genera un nuevo token.pkl")

    # Crea el cliente de Google Drive
    service = build('drive', 'v3', credentials=creds)
    return service

@app.post("/")
async def root():
    try:
        service = get_drive_service()
        
        # Subir archivo
        file_metadata = {
            'name': 'ejemplo.docx',
            'parents': ['1E4brfQPnwurTivj8mjpdAtc_ByprLbNL'] ## FOLDER_ID
        }
        media = MediaFileUpload('ejemplo.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
    
        print(f"✅ Archivo subido: {file.get('webViewLink')}")

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        print(f"Error al iniciar Uvicorn: {e}")
