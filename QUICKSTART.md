# 🚀 Guía de Inicio Rápido - Ad-Inspector Bot

Esta guía te llevará de **0 a funcionando en 5 minutos**.

---

## ✅ Prerrequisitos

Antes de empezar, asegúrate de tener instalado:

- ✅ **Python 3.11+** → [Descargar](https://www.python.org/downloads/)
- ✅ **Node.js 20+** → [Descargar](https://nodejs.org/)
- ✅ **Git** → [Descargar](https://git-scm.com/)
- ✅ **Google Gemini API Key** → [Obtener gratis](https://makersuite.google.com/app/apikey)

---

## 📦 Paso 1: Clonar el Proyecto

```bash
git clone https://github.com/tu-usuario/Ad-Inspector-Bot.git
cd Ad-Inspector-Bot
```

---

## 🔧 Paso 2: Configuración Automática

### Windows

```bash
start.bat
```

### Linux/Mac

```bash
chmod +x start.sh
./start.sh
```

El script automáticamente:
- ✅ Crea entorno virtual Python
- ✅ Instala todas las dependencias
- ✅ Instala navegadores Playwright
- ✅ Crea archivos .env desde templates
- ✅ Inicializa la base de datos

**Si el script pide API keys**, continúa con el paso 3.

---

## 🔑 Paso 3: Configurar API Keys

### 3.1 Backend (.env)

Edita `backend/.env`:

```env
# REQUERIDO: Google Gemini AI
GEMINI_API_KEY=tu_api_key_aqui

# OPCIONAL: Email (para alertas)
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password

# OPCIONAL: Slack (para alertas)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx
```

### 3.2 Frontend (.env.local)

Edita `.env.local`:

```env
VITE_GEMINI_API_KEY=tu_api_key_aqui
```

> 💡 **Tip**: Usa el mismo API key de Gemini para backend y frontend

---

## ▶️ Paso 4: Iniciar el Sistema

### Opción A: Script Automático

```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

### Opción B: Manual

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

**Terminal 2 (Frontend):**
```bash
npm run dev
```

---

## 🌐 Paso 5: Abrir Dashboard

Abre tu navegador en:

- 📊 **Dashboard**: [http://localhost:5173](http://localhost:5173)
- 🔌 **API**: [http://localhost:8000](http://localhost:8000)
- 📚 **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ✨ Paso 6: Crear tu Primera Campaña

### Desde el Dashboard (UI)

1. Click en **"Campaigns"** en el sidebar
2. Click en **"Add Campaign"**
3. Completa el formulario:
   - **Name**: Mi Primera Campaña
   - **URL**: https://tu-landing-page.com
   - **Viewports**: Desktop, Mobile
4. Click en **"Save"**

### Desde Configuración (JSON)

Edita `config/campaigns.json`:

```json
{
  "campaigns": [
    {
      "id": "test_001",
      "name": "Mi Primera Campaña",
      "url": "https://example.com",
      "enabled": true,
      "check_interval_minutes": 5,
      "viewports": ["desktop"],
      "actions": [
        {
          "type": "wait",
          "duration_ms": 2000
        },
        {
          "type": "scroll",
          "target": "bottom",
          "delay_ms": 2000
        }
      ],
      "expected_elements": [
        "body",
        "header"
      ],
      "alerts": {
        "critical": {
          "email": ["tu-email@company.com"],
          "slack": false
        }
      }
    }
  ]
}
```

**Guardar y reiniciar el backend** para que tome los cambios.

---

## 🎯 Paso 7: Verificar que Funciona

### Ver Logs en Tiempo Real

**Dashboard** → **"Live Logs"** tab

Deberías ver:
```
[2024-12-13 10:00:00] INFO  Scheduler: Starting check cycle
[2024-12-13 10:00:01] INFO  Checking "Mi Primera Campaña" (desktop)
[2024-12-13 10:00:05] PASS  200 OK - Load time: 1.2s
```

### Ejecutar Check Manual

**Dashboard** → **"Campaigns"** → Click en tu campaña → **"Run Now"**

En 10-30 segundos deberías ver los resultados.

---

## 🚨 Solución de Problemas

### ❌ Error: "GEMINI_API_KEY es requerido"

**Solución**: Edita `backend/.env` y agrega tu API key:
```env
GEMINI_API_KEY=tu_key_aqui
```

### ❌ Error: "playwright not found"

**Solución**:
```bash
cd backend
source venv/bin/activate
playwright install chromium
```

### ❌ Error: "Port 8000 already in use"

**Solución**: Cambia el puerto en `backend/.env`:
```env
API_PORT=8001
```

### ❌ El Dashboard no se conecta a la API

**Solución**: Verifica que ambos servicios estén corriendo y que el frontend apunte al puerto correcto.

---

## 📚 Próximos Pasos

Ahora que tienes todo funcionando:

1. 📖 Lee la [Documentación Completa](README_BACKEND.md)
2. 🎯 Configura campañas reales desde `config/campaigns.json`
3. 🔔 Configura alertas (Email, Slack, Telegram)
4. 🤖 Explora el análisis AI desde el dashboard
5. 🐳 Deploy en producción con Docker

---

## 💬 ¿Necesitas Ayuda?

- 📧 Email: support@ad-inspector.dev
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/Ad-Inspector-Bot/issues)
- 💬 Discord: [Unirse al servidor](https://discord.gg/ad-inspector)

---

## ✅ Checklist de Configuración

- [ ] Python 3.11+ instalado
- [ ] Node.js 20+ instalado
- [ ] Proyecto clonado
- [ ] Dependencias instaladas (backend y frontend)
- [ ] Playwright navegadores instalados
- [ ] API key de Gemini configurada
- [ ] Base de datos inicializada
- [ ] Backend corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 5173
- [ ] Dashboard accesible en navegador
- [ ] Primera campaña configurada
- [ ] Verificación manual ejecutada con éxito

Si completaste todos los puntos: **¡Felicitaciones! 🎉**

Tu **Ad-Inspector Bot** está listo para trabajar 24/7 protegiendo tu presupuesto publicitario.

---

<div align="center">

**Hecho con ❤️ para salvar presupuestos publicitarios**

[⬅️ Volver al README principal](README.md)

</div>
