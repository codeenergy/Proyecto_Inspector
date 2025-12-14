# 🚀 Guía de Deployment - Vercel + Railway

## ✅ Problemas Corregidos

1. **Error de importación del módulo en Railway** - SOLUCIONADO
2. **Archivo requirements-minimal.txt faltante** - CREADO
3. **Comando de inicio incorrecto** - CORREGIDO
4. **Login requiere refresh** - SOLUCIONADO

---

## 📋 Paso 1: Configurar Variables de Entorno en Railway

### Ve a tu proyecto en Railway:
URL: https://railway.app/project/[tu-proyecto]

### Configura estas variables en la pestaña "Variables":

```env
# REQUERIDO - Sin esto la app crasheará
ENVIRONMENT=production
GEMINI_API_KEY=tu-clave-real-aqui

# CORS - Actualiza con tu URL de Vercel
CORS_ORIGINS=https://proyecto-inspector.vercel.app,https://tu-app.vercel.app

# Base de datos
DATABASE_URL=sqlite:///./inspector.db
DB_ECHO=false

# API Configuration
API_HOST=0.0.0.0
LOG_LEVEL=INFO

# Browser (deshabilitado en Railway por falta de dependencias)
HEADLESS_BROWSER=true
ENABLE_AI_ANALYSIS=false
```

**IMPORTANTE:** Railway asigna automáticamente la variable `PORT`, no la configures manualmente.

---

## 📋 Paso 2: Configurar Variables de Entorno en Vercel

### Ve a tu proyecto en Vercel:
URL: https://vercel.com/[tu-usuario]/proyecto-inspector

### En Settings → Environment Variables, agrega:

**Variable Name:** `VITE_API_BASE_URL`
**Value:** `https://[tu-app].up.railway.app`
**Environment:** Production

**Ejemplo:**
```
VITE_API_BASE_URL=https://proyectoinspector-production.up.railway.app
```

---

## 📋 Paso 3: Hacer Push y Deploy

### 1. Commit los cambios:

```bash
git add .
git commit -m "Fix: Railway deployment - add requirements-minimal.txt and fix start command"
git push origin main
```

### 2. Railway deployará automáticamente

Verifica en Railway Dashboard → Deployments que:
- ✅ Build completa sin errores
- ✅ Logs muestran: "Uvicorn running on http://0.0.0.0:XXXX"
- ✅ Health check: `https://[tu-app].up.railway.app/health` devuelve 200

### 3. Redeploy Vercel

En Vercel Dashboard:
1. Ve a Deployments
2. Click en los "..." del último deployment
3. Selecciona "Redeploy"
4. Asegúrate que la variable `VITE_API_BASE_URL` esté configurada

---

## 🧪 Paso 4: Probar el Deployment

### Test 1: Health Check del Backend
```bash
curl https://[tu-app].up.railway.app/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "service": "traffic-bot-pro",
  "version": "2024.07.1",
  "scheduler_running": true
}
```

### Test 2: CORS
```bash
curl -X OPTIONS https://[tu-app].up.railway.app/targets \
  -H "Origin: https://proyecto-inspector.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

Deberías ver header: `Access-Control-Allow-Origin: https://proyecto-inspector.vercel.app`

### Test 3: Login en Vercel
1. Ve a `https://proyecto-inspector.vercel.app`
2. Login con:
   - Usuario: `codeenergy`
   - Password: `Codeenergy77##`
3. **Debería entrar INMEDIATAMENTE sin refresh**

### Test 4: Crear Target
1. Click en "Add Target"
2. URL: `https://example.com`
3. Click "Create Target"
4. **Debería crearse sin errores**
5. Abre DevTools (F12) y revisa logs en Console

---

## 🔍 Debugging

### Si Railway sigue fallando:

1. **Revisa los logs de Railway:**
   - Dashboard → Tu servicio → Deployments → Latest → View Logs
   - Busca errores de Python o missing modules

2. **Verifica que requirements-minimal.txt existe:**
   ```bash
   git ls-files backend/requirements-minimal.txt
   ```

3. **Verifica el start command en Railway:**
   - Settings → Deploy → Start Command debe ser auto-detectado de `railway.json`

### Si Vercel no conecta al backend:

1. **Verifica la URL del API:**
   - Settings → Environment Variables → `VITE_API_BASE_URL`
   - Debe ser la URL completa de Railway (sin trailing slash)

2. **Redeploy después de cambiar variables:**
   - Cambiar variables de entorno NO redeploya automáticamente
   - Debes hacer un redeploy manual

### Si el login sigue requiriendo refresh:

1. **Limpia el caché del navegador:**
   - Ctrl+Shift+Delete → Clear cache
   - O usa modo incógnito para probar

2. **Verifica la consola del navegador:**
   - F12 → Console
   - Busca errores de JavaScript

---

## 📊 Logs y Monitoreo

### Railway Logs
```bash
# Ver logs en tiempo real desde CLI (opcional)
railway logs --service [tu-servicio]
```

### Frontend Logs (Vercel)
- Dashboard → Tu proyecto → Deployments → Click en deployment → Logs

### Backend Logs (Railway)
- Dashboard → Tu servicio → Deployments → View Logs
- Busca líneas que empiecen con `INFO`, `ERROR`, `WARNING`

---

## ✅ Checklist de Deployment

- [ ] `backend/requirements-minimal.txt` existe en el repo
- [ ] Railway variables de entorno configuradas (mínimo: `GEMINI_API_KEY`, `CORS_ORIGINS`)
- [ ] Vercel variable `VITE_API_BASE_URL` configurada con URL de Railway
- [ ] Push a GitHub completado
- [ ] Railway deployment exitoso (sin errores en logs)
- [ ] Vercel redeployado después de configurar variables
- [ ] Health check del backend responde 200
- [ ] Login funciona sin refresh
- [ ] Crear target funciona sin errores de conexión

---

## 🆘 Si Nada Funciona

1. **Verifica los logs exactos** - Los errores específicos están ahí
2. **Prueba localmente primero:**
   ```bash
   cd backend
   pip install -r requirements-minimal.txt
   python init_database.py
   python -m uvicorn api.server:app --host 0.0.0.0 --port 8001
   ```
3. **Considera usar Render.com** como alternativa a Railway (guía en RAILWAY_DEBUG.md)

---

## 📞 Próximos Pasos

1. ✅ Push los cambios al repo
2. ✅ Configura variables en Railway
3. ✅ Configura variables en Vercel
4. ✅ Verifica que ambos deployments estén activos
5. ✅ Prueba login y crear targets
6. ✅ Revisa logs si hay errores

¡Listo! Tu app debería estar funcionando en producción.
