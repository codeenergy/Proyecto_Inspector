# 🎯 BOT MODO USUARIO NORMAL - Documentación

## ✅ CAMBIOS IMPLEMENTADOS

### 🚀 Funcionalidad Principal
El bot ahora funciona como un **usuario 100% normal** que:
- ✅ Hace clic en **TODOS los botones** de la página (no solo detecta ads)
- ✅ Detecta y abre **ventanas/pestañas nuevas** (incluyendo Monetag Direct Links)
- ✅ Espera **3-6 segundos** en ventanas nuevas (comportamiento humano realista)
- ✅ Hace **scroll** en ventanas nuevas antes de cerrarlas
- ✅ **Vuelve automáticamente** a la ventana principal
- ✅ **NO detecta ads** (actúa como usuario normal)

---

## 🔧 CAMBIOS TÉCNICOS

### Archivo: `backend/modules/user_simulator_undetected.py`

#### ❌ ELIMINADO:
- `detect_monetag_scripts()` - Ya no detecta scripts de ads

#### ✅ NUEVAS FUNCIONES:

**1. `find_all_buttons()`**
```python
# Busca TODOS los botones visibles en la página:
- <button>
- <a href>
- [role="button"]
- input[type="button"]
- input[type="submit"]
- [onclick]
- .btn, .button
```

**2. `click_all_buttons()`**
```python
# Hace clic en cada botón encontrado:
- Verifica visibilidad
- Click humano con offset aleatorio
- Detecta si se abren ventanas nuevas
- Espera entre clicks (1-2 segundos)
- Limita a 10 botones por selector
```

**3. `handle_new_windows(wait_time=(3, 6))`**
```python
# Maneja ventanas/pestañas nuevas:
- Cambia a la ventana nueva
- Espera 3-6 segundos (configurable)
- Hace scroll (300px en 3 pasos)
- Cierra la ventana
- Vuelve a ventana principal
```

**4. `detect_monetag_links()`**
```python
# Detecta enlaces directos de Monetag:
- monetag, gizokraijaw
- 3nbf4.com, nap5k.com
- otieu.com, thubanoa.com
```

---

## 📊 FLUJO DE TRABAJO

```
1. Navegar a página principal
   ↓
2. Esperar carga (4-7 segundos)
   ↓
3. Scroll natural (400-800px)
   ↓
4. Buscar TODOS los botones visibles
   ↓
5. Para cada botón:
   ├─ Click humano
   ├─ Si se abre ventana nueva:
   │  ├─ Cambiar a ventana
   │  ├─ Esperar 3-6 segundos
   │  ├─ Hacer scroll
   │  ├─ Cerrar ventana
   │  └─ Volver a ventana principal
   └─ Esperar 1-2 segundos
   ↓
6. Navegar a página interna (excluyendo Monetag)
   ↓
7. Repetir desde paso 3
```

---

## 📈 ESTADÍSTICAS NUEVAS

El bot ahora reporta:
```javascript
{
  "pages_visited": 8,        // Páginas internas visitadas
  "buttons_clicked": 42,     // Total de botones clickeados
  "windows_opened": 15       // Ventanas/pestañas abiertas
}
```

---

## ⚙️ CONFIGURACIÓN

### Variables de configuración:
```python
config = {
    "url": "https://tu-sitio.com",
    "target_pageviews": 8,                    # Páginas a visitar
    "viewport": {"width": 1920, "height": 1080}
}
```

### Tiempos de espera (configurables en código):
- **Carga página**: 4-7 segundos
- **Entre clicks**: 1-2 segundos
- **Ventanas nuevas**: 3-6 segundos ⭐ (comportamiento humano)
- **Navegación**: 3-5 segundos

---

## 🔄 COMPATIBILIDAD

### Dependencias actualizadas:
```txt
undetected-chromedriver==3.5.4  # (downgrade de 3.5.5)
selenium==4.9.0                  # (downgrade de 4.17.2)
setuptools>=65.0.0              # (nuevo - Python 3.13 compatible)
```

### Razón del cambio:
- `undetected-chromedriver 3.5.5` + `selenium 4.17.2` tiene un bug
- `undetected-chromedriver 3.5.4` + `selenium 4.9.0` es estable

---

## 🎨 FRONTEND RESPONSIVE

El frontend ya está **100% responsive** con:

### Breakpoints:
- `sm:` 640px - Móviles horizontal / Tablets pequeñas
- `md:` 768px - Tablets
- `lg:` 1024px - Laptops
- `xl:` 1280px - Desktop

### Características:
✅ Menú móvil hamburguesa (`Menu` icon)
✅ Grid adaptativo:
  - Móvil: 1 columna
  - Tablet: 2 columnas
  - Desktop: 4 columnas
✅ Sidebar colapsable en móvil
✅ Tablas → Cards en móvil
✅ Botones adaptados con texto oculto en móvil
✅ Header sticky con controles adaptativos

---

## 🚀 DEPLOY

### Railway (Backend)
```bash
# Configuración automática vía:
- railway.json (Dockerfile builder)
- nixpacks.toml (Chromium + Playwright)
```

El bot detectará automáticamente el push a Git y redesplegará.

### Vercel (Frontend)
```bash
# Configuración automática vía:
- vercel.json (Vite + SPA rewrites)
```

El frontend también se redesplega automáticamente.

---

## 📝 TESTING

### Archivo de test incluido:
```bash
python test_simple.py
```

**Nota**: Requiere Chrome instalado localmente. En producción (Railway) usará Chromium automáticamente.

---

## 🎯 EJEMPLO DE USO

```python
from backend.modules.user_simulator_undetected import run_undetected_session

config = {
    "url": "https://cofreprompt.com",
    "target_pageviews": 5,
    "viewport": {"width": 1920, "height": 1080}
}

result = await run_undetected_session(config)

# Resultado:
{
    "success": True,
    "stats": {
        "pages_visited": 5,
        "buttons_clicked": 28,
        "windows_opened": 12
    },
    "log": [...]
}
```

---

## ⚡ VENTAJAS DEL NUEVO SISTEMA

1. **Más natural**: Actúa como usuario real, no como bot
2. **Más clicks**: Clickea TODOS los botones, no solo detecta ads
3. **Monetización optimizada**: Abre Direct Links de Monetag automáticamente
4. **Comportamiento humano**: Esperas realistas, scroll, navegación natural
5. **Sin detección**: No busca ads específicamente, solo navega
6. **Responsive**: Frontend funciona perfecto en móvil/tablet/desktop

---

## 🔗 COMMIT

```
Commit: 29f185e
Mensaje: 🎯 BOT MODO USUARIO NORMAL: Click en TODOS los botones + Monetag Direct Links
```

---

## 📞 SOPORTE

Para problemas o preguntas, revisar los logs en:
- Railway: Dashboard → Logs
- Local: Consola del script de test

---

**Última actualización**: 2025-12-24
**Versión**: 2.0.0 - Modo Usuario Normal
