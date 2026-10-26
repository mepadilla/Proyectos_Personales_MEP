# Usamos una imagen ligera de Python
FROM python:3.10-slim

# Permitir que los mensajes de log de Python lleguen a la consola de Cloud Logging
ENV PYTHONUNBUFFERED True

# 1. Instalar dependencias del sistema para WeasyPrint y Gunicorn
# Necesitamos Pango, Cairo y fuentes para que el PDF se genere correctamente
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz-subset0 \
    libjpeg-dev \
    libopenjp2-7-dev \
    libcairo2 \
    libffi-dev \
    # Fuentes para que el PDF tenga texto legible
    fonts-dejavu \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# 2. Configurar directorio de trabajo
ENV APP_HOME /app
WORKDIR $APP_HOME

# 3. Copiar dependencias e instalarlas
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el código de la aplicación
COPY . ./

# 5. Ejecutar la aplicación con Gunicorn (Servidor de Producción)
# Cloud Run inyecta la variable de entorno PORT (por defecto 8080)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app