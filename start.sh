#!/bin/bash

# Script de inicio rápido para Ad-Inspector Bot
# Uso: ./start.sh [development|production]

set -e

MODE=${1:-development}

echo "=========================================="
echo "🤖 Ad-Inspector Bot - Startup Script"
echo "=========================================="
echo "Modo: $MODE"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar dependencias
echo "🔍 Verificando dependencias..."

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 no encontrado${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}❌ Node.js no encontrado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependencias verificadas${NC}"
echo ""

# Backend setup
echo "🐍 Configurando Backend Python..."

cd backend

# Crear venv si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar venv
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Instalar dependencias
echo "Instalando dependencias Python..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Instalar Playwright browsers
echo "Instalando navegadores Playwright..."
playwright install chromium

# Verificar .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Archivo .env no encontrado${NC}"
    echo "Copiando .env.example a .env..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Por favor, edita backend/.env con tus API keys antes de continuar${NC}"
    exit 1
fi

# Inicializar DB si no existe
if [ ! -f "inspector.db" ]; then
    echo "Inicializando base de datos..."
    python init_database.py --seed
fi

cd ..

echo -e "${GREEN}✅ Backend configurado${NC}"
echo ""

# Frontend setup
echo "⚛️  Configurando Frontend React..."

# Instalar dependencias si no existen
if [ ! -d "node_modules" ]; then
    echo "Instalando dependencias Node..."
    npm install
fi

# Verificar .env.local
if [ ! -f ".env.local" ]; then
    echo -e "${YELLOW}⚠️  Archivo .env.local no encontrado${NC}"
    echo "Copiando .env.example a .env.local..."
    cp .env.example .env.local
    echo -e "${YELLOW}⚠️  Por favor, edita .env.local con tu GEMINI_API_KEY${NC}"
fi

echo -e "${GREEN}✅ Frontend configurado${NC}"
echo ""

# Iniciar servicios
echo "🚀 Iniciando servicios..."
echo ""

if [ "$MODE" = "production" ]; then
    echo "Modo Producción - Usando Docker Compose"
    docker-compose up -d
    echo ""
    echo -e "${GREEN}✅ Servicios iniciados con Docker${NC}"
    echo ""
    echo "📊 Dashboard: http://localhost"
    echo "🔌 API: http://localhost:8000"
    echo ""
    echo "Ver logs: docker-compose logs -f"
    echo "Detener: docker-compose down"
else
    echo "Modo Desarrollo - Iniciando servicios localmente"
    echo ""

    # Función para cleanup al salir
    cleanup() {
        echo ""
        echo "🛑 Deteniendo servicios..."
        kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
        exit 0
    }

    trap cleanup SIGINT SIGTERM

    # Iniciar backend
    echo "Iniciando Backend (Puerto 8000)..."
    cd backend
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
    python main.py &
    BACKEND_PID=$!
    cd ..

    sleep 3

    # Iniciar frontend
    echo "Iniciando Frontend (Puerto 5173)..."
    npm run dev &
    FRONTEND_PID=$!

    sleep 2

    echo ""
    echo -e "${GREEN}✅ Servicios iniciados${NC}"
    echo ""
    echo "=========================================="
    echo "📊 Dashboard: http://localhost:5173"
    echo "🔌 API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo "=========================================="
    echo ""
    echo "Presiona Ctrl+C para detener todos los servicios"
    echo ""

    # Mantener vivo
    wait
fi
