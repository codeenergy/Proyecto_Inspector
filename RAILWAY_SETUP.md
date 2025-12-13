# 🚂 Railway Setup - Pasos EXACTOS para Desplegar Backend

## ❌ Problema Actual
Railway está sirviendo el frontend (React) en lugar del backend (Python API).

## ✅ Solución: 3 Pasos Simples

---

### **PASO 1: Configurar Root Directory**

1. Abre [Railway Dashboard](https://railway.app/dashboard)
2. Selecciona tu proyecto: `proyectoinspector-production`
3. Click en tu servicio (el que está desplegado)
4. Ve a la pestaña **"Settings"** (⚙️)
5. Scroll hasta encontrar **"Root Directory"**
6. Escribe: `backend`
7. Click **"Update"** o presiona Enter
8. ✅ Confirmación: Railway dirá "Root directory updated"

---

### **PASO 2: Agregar Variables de Entorno**

1. En el mismo servicio, ve a la pestaña **"Variables"** (🔑)
2. Click **"New Variable"**
3. Agrega UNA POR UNA estas variables:

```
Variable 1:
Name: GEMINI_API_KEY
Value: AIzaSyCGzdNBfM2_zDp3QkjkwfS3UeKcktghaIY

Variable 2:
Name: ENVIRONMENT
Value: production

Variable 3:
Name: CORS_ORIGINS
Value: https://proyecto-inspector.vercel.app

Variable 4:
Name: LOG_LEVEL
Value: INFO

Variable 5:
Name: DATABASE_URL
Value: sqlite:///./inspector.db
```

4. Click **"Add"** después de cada una

---

### **PASO 3: Forzar Redeploy**

1. Ve a la pestaña **"Deployments"** (📦)
2. Verás una lista de deployments
3. El primero de la lista es el más reciente
4. Click en los **tres puntos (⋮)** al lado derecho
5. Click **"Redeploy"**
6. Espera 2-3 minutos

---

## ✅ Verificación

Después del redeploy, prueba:

```bash
curl https://proyectoinspector-production.up.railway.app/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "service": "traffic-bot-pro",
  "version": "2024.07.1",
  "scheduler_running": true
}
```

---

## 🔴 Si SIGUE sin funcionar

### Opción A: Eliminar y crear nuevo servicio

1. En Railway Dashboard → Settings → **"Danger"** → **"Remove Service"**
2. Confirmar eliminación
3. Click **"+ New"** → **"GitHub Repo"**
4. Seleccionar: `codeenergy/Proyecto_Inspector`
5. **MUY IMPORTANTE**: Cuando pregunte por Root Directory, escribir: `backend`
6. Agregar las variables de entorno (ver Paso 2)
7. Desplegar

### Opción B: Usar Render.com en lugar de Railway

1. Ve a [Render.com](https://render.com)
2. Crear cuenta / Login
3. **New** → **Web Service**
4. Conectar GitHub: `codeenergy/Proyecto_Inspector`
5. Configuración:
   - **Name**: proyecto-inspector-backend
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements-minimal.txt`
   - **Start Command**: `python -m api.server`
6. **Environment Variables**: Agregar las 5 variables del Paso 2
7. Click **"Create Web Service"**

---

## 📊 Resumen del Estado Actual

✅ Código backend completamente funcional
✅ Detección de Monetag optimizada (Push, Vignette, In-Page Push, Direct Link)
✅ API endpoints listos (/health, /targets, /stats, etc.)
✅ Archivos de configuración Railway creados (nixpacks.toml, railway.toml)
❌ Railway configurado incorrectamente (sirviendo frontend en lugar de backend)

**La solución es SOLO configuración de Railway, no código.**

---

## 🆘 Si necesitas ayuda

1. Toma screenshot de Railway Settings (mostrando Root Directory)
2. Toma screenshot de Railway Variables
3. Toma screenshot de Railway Deployment logs (los últimos 50 líneas)
