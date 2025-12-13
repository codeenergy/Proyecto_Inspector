# 🚀 Deployment Guide - TrafficBot Pro

## 🔴 Solución al "Connection Error"

El error **"Connection error"** al crear targets ocurre porque:
- ✅ Frontend desplegado en Vercel: `https://proyecto-inspector.vercel.app`
- ❌ Backend NO desplegado (solo en `localhost:8001`)
- ❌ Frontend no puede conectarse al backend → **Connection Error**

## ✅ Solución: Deploy Backend + Configurar Vercel

---

## 📋 Pasos para Desplegar

### 1. Desplegar el Backend

El backend Python necesita estar alojado en un servidor separado. **Opciones recomendadas**:

#### Opción A: Railway.app (Recomendado)

1. Crear cuenta en [Railway.app](https://railway.app)
2. Instalar Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```
3. Desde la carpeta `backend/`:
   ```bash
   railway login
   railway init
   railway up
   ```
4. Configurar variables de entorno en Railway:
   - `GEMINI_API_KEY`: Tu API key de Gemini
   - `ENVIRONMENT`: production
   - `CORS_ORIGINS`: https://proyecto-inspector.vercel.app

#### Opción B: Render.com

1. Crear cuenta en [Render.com](https://render.com)
2. Crear nuevo "Web Service"
3. Conectar repositorio
4. Configurar:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && python main.py`
   - **Environment**: Python 3.11+

#### Opción C: Fly.io

1. Instalar Fly CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Desde la carpeta `backend/`:
   ```bash
   fly launch
   fly deploy
   ```

### 2. Actualizar Variables de Entorno

Una vez que tengas la URL del backend desplegado (ejemplo: `https://tu-app.railway.app`):

1. **Localmente**: Actualiza `.env.production`:
   ```env
   VITE_API_BASE_URL=https://tu-app.railway.app
   ```

2. **En Vercel**: 
   - Ve a tu proyecto en Vercel Dashboard
   - Settings → Environment Variables
   - Agrega: `VITE_API_BASE_URL` = `https://tu-app.railway.app`
   - Marca para "Production"

### 3. Redesplegar Frontend

```bash
# Construir con las nuevas variables
npm run build

# Desplegar a Vercel
vercel --prod
```

O simplemente hacer push a tu repositorio si tienes auto-deploy configurado.

---

## 🧪 Verificación

### Local (Desarrollo)
```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
npm run dev
```

Abrir http://localhost:5174 y verificar que puedes crear targets.

### Producción

1. Visitar https://proyecto-inspector.vercel.app
2. Intentar crear un nuevo target
3. Verificar que no aparece "Connection error"
4. Revisar que el dashboard muestra datos correctamente

---

## 🔧 Comandos Útiles

### Frontend
```bash
# Desarrollo
npm run dev

# Build de producción
npm run build

# Preview del build
npm run preview
```

### Backend
```bash
# Desarrollo
cd backend
python main.py

# Con variables de entorno específicas
ENVIRONMENT=production python main.py
```

---

## 📝 Notas Importantes

1. **Variables de Entorno**: Los archivos `.env` y `.env.production` están en `.gitignore` por seguridad
2. **CORS**: El backend ya está configurado para aceptar requests desde `https://proyecto-inspector.vercel.app`
3. **API Key**: Asegúrate de configurar `GEMINI_API_KEY` en el backend de producción
4. **Puerto**: El backend por defecto usa el puerto 8000, pero Railway/Render asignan automáticamente

---

## 🐛 Troubleshooting

### Error: "Connection error" persiste
- Verifica que `VITE_API_BASE_URL` esté configurada en Vercel
- Confirma que el backend esté corriendo (visita la URL del backend directamente)
- Revisa los logs del backend para errores CORS

### Error: "CORS policy"
- Verifica que la URL del frontend esté en `CORS_ORIGINS` del backend
- Asegúrate de incluir el protocolo (`https://`) en la configuración

### Backend no inicia
- Revisa que todas las dependencias estén instaladas: `pip install -r requirements.txt`
- Verifica que `GEMINI_API_KEY` esté configurada
- Revisa los logs del servicio de hosting
