FROM python:3.11-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium-driver \
    chromium

# Instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código
COPY . /app
WORKDIR /app

# Crea la carpeta de descargas
RUN mkdir -p /app/downloads

# Ejecuta el script principal
CMD ["python", "rpa_login.py"] 