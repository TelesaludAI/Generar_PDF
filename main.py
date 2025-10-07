from fastapi import FastAPI
from fastapi.responses import FileResponse
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Servidor en Railway funcionando correctamente ✅"}

@app.get("/generar")
def generar_documentos():
    # Crear documento Word
    doc = Document()
    doc.add_heading("Ejemplo de Documento", level=1)
    doc.add_paragraph("Este documento fue generado desde FastAPI y Python en Railway.")
    
    # Agregar firma
    if os.path.exists("firma.png"):
        doc.add_picture("firma.png", width=2000000)  # ~2 cm
        doc.add_paragraph("Firma digital")
    
    docx_filename = "documento.docx"
    pdf_filename = "documento.pdf"
    doc.save(docx_filename)

    # Crear PDF con reportlab (texto plano)
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 100, "Ejemplo de Documento")
    c.drawString(100, height - 120, "Este documento fue generado desde FastAPI y Python en Railway.")
    
    if os.path.exists("firma.png"):
        c.drawImage("firma.png", 100, height - 200, width=100, height=50)
        c.drawString(100, height - 210, "Firma digital")

    c.save()

    return FileResponse(pdf_filename, media_type="application/pdf", filename=pdf_filename)
