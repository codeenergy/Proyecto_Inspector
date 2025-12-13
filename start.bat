@echo off
REM Script de inicio para Windows
REM Uso: start.bat [development|production]

setlocal

set MODE=%1
if "%MODE%"=="" set MODE=development

echo ==========================================
echo Ad-Inspector Bot - Startup Script
echo ==========================================
echo Modo: %MODE%
echo.

REM Verificar Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no encontrado
    exit /b 1
)

REM Verificar Node
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js no encontrado
    exit /b 1
)

echo [OK] Dependencias verificadas
echo.

REM Backend setup
echo Configurando Backend Python...
cd backend

REM Crear venv si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar venv
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Instalando dependencias Python...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Instalar Playwright
echo Instalando navegadores Playwright...
playwright install chromium

REM Verificar .env
if not exist ".env" (
    echo [WARNING] Archivo .env no encontrado
    echo Copiando .env.example a .env...
    copy .env.example .env
    echo [WARNING] Edita backend\.env con tus API keys antes de continuar
    pause
    exit /b 1
)

REM Inicializar DB
if not exist "inspector.db" (
    echo Inicializando base de datos...
    python init_database.py --seed
)

cd ..

echo [OK] Backend configurado
echo.

REM Frontend setup
echo Configurando Frontend React...

if not exist "node_modules" (
    echo Instalando dependencias Node...
    call npm install
)

if not exist ".env.local" (
    echo [WARNING] Archivo .env.local no encontrado
    copy .env.example .env.local
    echo [WARNING] Edita .env.local con tu GEMINI_API_KEY
)

echo [OK] Frontend configurado
echo.

REM Iniciar servicios
echo Iniciando servicios...
echo.

if "%MODE%"=="production" (
    echo Modo Produccion - Usando Docker Compose
    docker-compose up -d
    echo.
    echo [OK] Servicios iniciados con Docker
    echo.
    echo Dashboard: http://localhost
    echo API: http://localhost:8000
    echo.
    echo Ver logs: docker-compose logs -f
    echo Detener: docker-compose down
) else (
    echo Modo Desarrollo - Iniciando servicios localmente
    echo.

    REM Iniciar backend en nueva ventana
    start "Ad-Inspector Backend" cmd /k "cd backend && venv\Scripts\activate && python main.py"

    timeout /t 3 /nobreak >nul

    REM Iniciar frontend en nueva ventana
    start "Ad-Inspector Frontend" cmd /k "npm run dev"

    timeout /t 2 /nobreak >nul

    echo.
    echo [OK] Servicios iniciados
    echo.
    echo ==========================================
    echo Dashboard: http://localhost:5173
    echo API: http://localhost:8000
    echo API Docs: http://localhost:8000/docs
    echo ==========================================
    echo.
    echo Las ventanas de Backend y Frontend se abrieron por separado
    echo Cierra las ventanas para detener los servicios
    echo.
)

endlocal
