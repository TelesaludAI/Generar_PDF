from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from docx import Document
from docx.shared import Inches
import pypandoc
import os

app = FastAPI(title="API de generación de documentos")

DOCX_FILE = "documento_generado.docx"
PDF_FILE = "documento_generado.pdf"
FIRMA_IMG = "firma.png"


@app.get("/")
def home():
    return {"message": "✅ API de generación de documentos con FastAPI activa"}


@app.get("/generar")
def generar_documentos():
    """Genera un documento Word y su versión en PDF."""
    try:
        doc = Document()
        doc.add_heading("Informe de Servicio", level=1)
        doc.add_paragraph("Este documento fue generado automáticamente desde Python con FastAPI.")
        doc.add_paragraph("Firma del responsable:")

        if os.path.exists(FIRMA_IMG):
            doc.add_picture(FIRMA_IMG, width=Inches(2))
        else:
            doc.add_paragraph("⚠️ Firma no disponible (imagen no encontrada).")

        doc.save(DOCX_FILE)

        # Convertir a PDF con Pandoc
        try:
            pypandoc.convert_file(
                DOCX_FILE,
                'pdf',
                outputfile=PDF_FILE,
                extra_args=['--pdf-engine=xelatex']
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al convertir a PDF: {str(e)}")

        return {"message": "✅ Documentos generados correctamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/descargar/docx")
def descargar_docx():
    """Permite descargar el documento Word."""
    if not os.path.exists(DOCX_FILE):
        raise HTTPException(status_code=404, detail="El documento DOCX no existe")
    return FileResponse(DOCX_FILE, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=DOCX_FILE)


@app.get("/descargar/pdf")
def descargar_pdf():
    """Permite descargar el documento PDF."""
    if not os.path.exists(PDF_FILE):
        raise HTTPException(status_code=404, detail="El documento PDF no existe")
    return FileResponse(PDF_FILE, media_type="application/pdf", filename=PDF_FILE)
