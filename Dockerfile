# Imagen base de Python ligera
FROM python:3.10-slim

# Instalar dependencias esenciales y Pandoc
RUN apt-get update &&     apt-get install -y pandoc &&     apt-get clean &&     rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto
EXPOSE 8080

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
