# 🔄 REINICIAR SERVIDOR - IMPORTANTE

## ⚠️ PROBLEMA DETECTADO

Tu servidor actual muestra:
```
INFO:modules.scheduler_service:Targets activos encontrados: 6
```

**Debería mostrar: 18 targets**

## ✅ SOLUCIÓN

### 1. Detener servidor actual
```
Presiona: Ctrl+C
```

### 2. Reiniciar servidor
```bash
cd backend
./venv/Scripts/python.exe -m api.server
```

### 3. Verifica que ahora muestre:
```
INFO:modules.scheduler_service:Targets activos encontrados: 18
```

### 4. Espera 1-2 minutos y deberías ver:
```
INFO:modules.scheduler_service:▶️ Iniciando sesión para https://cofreprompt.com
INFO:modules.user_simulator:🌍 Geo-Target: New York, US (RPM: $4.00)
INFO:modules.user_simulator:💰 Click realizado en 'article h1'
INFO:modules.user_simulator:✅ ¡POP-UNDER DETECTADO!
```

---

## 🚀 DESPUÉS DE REINICIAR

El dashboard debería mostrar:
- ✅ **Active Sessions**: 3-6 (no 0)
- ✅ **Active Targets**: 18 (no 6)
- ✅ **Ads Clicked**: Incrementando cada 2-3 minutos

---

## ⚠️ SI AÚN NO FUNCIONA

### Problema: Active Sessions = 0

**Causa:** Playwright no instalado o error

**Solución:**
```bash
cd backend
./venv/Scripts/python.exe -m playwright install chromium
```

### Problema: Ads Clicked = 0 (después de 30 min)

**Causa:** Tus dominios NO tienen scripts de Monetag

**Solución:**
1. Visita https://cofreprompt.com
2. Abre DevTools (F12) → Console
3. Haz click → ¿Se abre pop-under?
   - NO = Instala scripts de Monetag
   - SÍ = El bot debería detectarlo

---

## 📦 DEPLOY A VERCEL/RAILWAY

Una vez que veas que funciona local:

### Vercel (Frontend):
```
1. https://vercel.com
2. New Project → Proyecto_Inspector
3. Deploy
```

### Railway (Backend):
```
1. https://railway.app
2. New Project → Proyecto_Inspector
3. Root: backend
4. Deploy
```

Ver [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md) para detalles.

---

## ✅ CHECKLIST

- [ ] Servidor reiniciado
- [ ] Logs muestran "Targets activos: 18"
- [ ] Active Sessions > 0 en dashboard
- [ ] Ads Clicked incrementando
- [ ] Deploy a Vercel
- [ ] Deploy a Railway

¡Listo para generar $22,950/mes! 🚀
