# Railway Dockerfile para TrafficBot Pro
# Usar imagen oficial de Playwright que incluye todas las dependencias del sistema
FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de requirements
COPY backend/requirements-full.txt backend/requirements-full.txt

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r backend/requirements-full.txt

# Copiar el resto del código
COPY . .

# Inicializar base de datos (permite fallar)
RUN cd backend && python init_database.py || true

# Cambiar al directorio backend
WORKDIR /app/backend

# Exponer puerto (Railway usa la variable $PORT)
EXPOSE 8080

# Comando de inicio - usar script que respeta PORT env var
CMD ["python", "railway-start.py"]
