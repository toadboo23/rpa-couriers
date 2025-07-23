FROM python:3.11-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium-driver \
    chromium \
    cron

# Instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código
COPY . /app
WORKDIR /app

# Crea la carpeta de descargas y logs
RUN mkdir -p /app/downloads /logs

# Copia el archivo de cron
COPY mycron /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron

# Ejecuta cron en primer plano
CMD ["cron", "-f"] 