from fastapi import FastAPI
from fastapi.responses import JSONResponse
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# === CONFIGURACIÓN ===
SERVICE_ACCOUNT_FILE = "credentials.json"  # archivo descargado de Google Cloud
FOLDER_ID = "1E4brfQPnwurTivj8mjpdAtc_ByprLbNL"        # ID de la carpeta de Drive

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API activa ✅"}

@app.get("/generar")
def generar_documento(nombre: str = "documento"):
    docx_filename = f"{nombre}.docx"
    pdf_filename = f"{nombre}.pdf"

    # === Generar archivo DOCX ===
    doc = Document()
    doc.add_heading("Documento generado automáticamente", level=1)
    doc.add_paragraph("Este documento fue creado desde FastAPI en Railway y subido a Google Drive.")
    doc.save(docx_filename)

    ## === Generar PDF ===
    #c = canvas.Canvas(pdf_filename, pagesize=letter)
    #width, height = letter
    #c.setFont("Helvetica", 12)
    #c.drawString(100, height - 100, "Documento PDF generado automáticamente")
    #c.save()

    # === Subir DOCX a Google Drive ===
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": os.path.basename(docx_filename), "parents": [FOLDER_ID]}
    media = MediaFileUpload(docx_filename, mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    file = service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()

    return JSONResponse({
        "message": "✅ Documento generado y subido a Google Drive.",
        "drive_file_id": file.get("id"),
        "drive_link": file.get("webViewLink")
    })

