# Imagen base con Python
FROM python:3.10-slim

# Instalar dependencias necesarias para Pandoc y LaTeX
RUN apt-get update &&     apt-get install -y wget gnupg software-properties-common &&     apt-get install -y pandoc texlive-xetex texlive-fonts-recommended texlive-latex-recommended &&     apt-get clean &&     rm -rf /var/lib/apt/lists/*

# Verificar instalación de pandoc
RUN pandoc --version

# Crear carpeta de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto (para Railway / FastAPI)
EXPOSE 8080

# Ejecutar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
