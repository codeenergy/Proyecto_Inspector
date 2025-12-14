# 🔧 FIX RAILWAY CRASH - SOLUCIÓN RÁPIDA

## ✅ Cambios Realizados

1. **Creado** `backend/start.sh` - Script de inicio robusto
2. **Creado** `backend/requirements-minimal.txt` - Dependencias mínimas
3. **Actualizado** `railway.json`, `railway.toml`, `Procfile` - Comandos correctos
4. **Actualizado** `backend/config.py` - Sin crash si falta GEMINI_API_KEY en prod

---

## 📋 PASOS RÁPIDOS (5 minutos)

### 1️⃣ CONFIGURA RAILWAY

Ve a: **Railway Dashboard → Tu Proyecto → Variables**

Agrega estas 3 variables MÍNIMAS:

```env
ENVIRONMENT=production
ENABLE_AI_ANALYSIS=false
CORS_ORIGINS=https://proyecto-inspector.vercel.app
```

> ⚠️ **IMPORTANTE:** Con `ENABLE_AI_ANALYSIS=false` NO necesitas GEMINI_API_KEY

**Opcional (si quieres AI):**
```env
ENABLE_AI_ANALYSIS=true
GEMINI_API_KEY=tu_clave_aqui
```

### 2️⃣ PUSH AL REPO

```bash
git add .
git commit -m "Fix: Railway crash - add start.sh script"
git push origin main
```

### 3️⃣ ESPERA EL DEPLOY

Railway deployará automáticamente. Espera 1-2 minutos.

**Verifica en Railway:**
- Build Logs: Debe mostrar "Successfully installed fastapi..."
- Deploy Logs: Debe mostrar "✅ Starting API server on PORT=XXXX..."
- Status: Debe estar en verde

### 4️⃣ PRUEBA EL BACKEND

Abre en tu navegador:
```
https://TU-APP.up.railway.app/health
```

Debes ver:
```json
{"status":"healthy","service":"traffic-bot-pro"}
```

### 5️⃣ CONFIGURA VERCEL

**Vercel Dashboard → Settings → Environment Variables:**

- Name: `VITE_API_BASE_URL`
- Value: `https://TU-APP.up.railway.app`
- Environment: ✅ Production

Luego **Redeploy** en Vercel.

---

## ✅ VERIFICACIÓN FINAL

1. **Backend Health:** https://TU-APP.up.railway.app/health → ✅ 200 OK
2. **Frontend:** https://proyecto-inspector.vercel.app → ✅ Login funciona
3. **Crear Target:** Click "Add Target" → ✅ Sin errores

---

## 🐛 Si SIGUE Crasheando

### Ver logs en Railway:
1. Dashboard → Deployments → Latest
2. Click "View Logs"
3. Busca líneas con `ERROR`

### Errores Comunes:

**Error:** `ModuleNotFoundError: No module named 'X'`
**Solución:** Verifica que `requirements-minimal.txt` tenga todas las deps

**Error:** `Address already in use`
**Solución:** Railway asigna PORT automáticamente, no la configures

**Error:** `GEMINI_API_KEY is required`
**Solución:** Agrega variable `ENABLE_AI_ANALYSIS=false` en Railway

---

## 📞 Última Opción

Si Railway sigue fallando después de estos pasos, copia el error EXACTO de los logs y avísame.

---

**Tiempo estimado:** 5 minutos ⏱️
**Dificultad:** ⭐ Fácil
