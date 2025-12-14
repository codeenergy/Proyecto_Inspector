# Railway Dockerfile para TrafficBot Pro
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requirements
COPY backend/requirements-full.txt backend/requirements-full.txt

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r backend/requirements-full.txt

# Instalar Playwright Chromium (sin system deps para evitar problemas)
RUN playwright install chromium

# Copiar el resto del código
COPY . .

# Hacer ejecutable el script de inicio
RUN chmod +x backend/start.sh

# Inicializar base de datos (permite fallar)
RUN cd backend && python init_database.py || true

# Cambiar al directorio backend
WORKDIR /app/backend

# Exponer puerto (Railway usa la variable $PORT)
EXPOSE 8080

# Comando de inicio
CMD ["./start.sh"]
