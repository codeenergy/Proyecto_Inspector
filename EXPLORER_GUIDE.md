# 🕵️ Guía del Explorador Web

## ¿Qué hace el Explorador Web?

El **Explorador Web** simula un usuario real navegando un dominio completo. NO solo revisa si una página funciona, sino que:

✅ **Navega como usuario real** - Scroll, movimientos de mouse, tiempos de lectura
✅ **Hace click en TODO** - Botones, enlaces, CTAs
✅ **Detecta y hace click en ANUNCIOS** - Google Ads, Facebook Ads, banners
✅ **Explora enlaces internos** - Navega por todo el sitio
✅ **Detecta formularios** - Identifica campos de contacto, registro, etc.
✅ **Toma screenshots** - Captura visual de cada página
✅ **Mapea el sitio completo** - Te da un mapa de todas las páginas

---

## 🚀 Formas de Usar

### Opción 1: Script de Python (Más Rápido)

```bash
cd backend
./venv/Scripts/activate
python explore_demo.py https://ejemplo.com
```

**Ejemplo:**
```bash
python explore_demo.py https://amazon.com
```

Esto te mostrará:
- Cuántas páginas visitó
- Cuántos botones clickeó
- **Cuántos anuncios encontró**
- Todos los enlaces que siguió

### Opción 2: API REST

Con el backend corriendo ([http://localhost:8000](http://localhost:8000)), usa:

**Con cURL:**
```bash
curl -X POST http://localhost:8000/explore/website \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://ejemplo.com",
    "max_depth": 2,
    "max_pages": 30,
    "viewport": "desktop"
  }'
```

**Con Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/explore/website",
    json={
        "url": "https://mercadolibre.com",
        "max_depth": 2,
        "max_pages": 50
    }
)

result = response.json()
print(f"Anuncios encontrados: {result['data']['total_ads_found']}")
```

**Con Postman:**
```
POST http://localhost:8000/explore/website
Body (JSON):
{
  "url": "https://tu-sitio.com",
  "max_depth": 3,
  "max_pages": 100
}
```

### Opción 3: Desde el Código Python

```python
import asyncio
from modules.web_explorer import explore_website

async def explorar():
    resultado = await explore_website(
        url="https://ejemplo.com",
        max_depth=2,
        max_pages=30
    )

    print(f"Páginas visitadas: {resultado['total_pages_visited']}")
    print(f"Anuncios encontrados: {resultado['total_ads_found']}")
    print(f"Botones clickeados: {resultado['total_buttons_clicked']}")

asyncio.run(explorar())
```

---

## 🎯 Parámetros

| Parámetro | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| `url` | URL del dominio a explorar | **Requerido** |
| `max_depth` | Profundidad de navegación (niveles de enlaces) | 2 |
| `max_pages` | Máximo de páginas a visitar | 30 |
| `viewport` | Tipo de dispositivo (`desktop`, `mobile`, `tablet`) | `desktop` |

### Ejemplos:

**Exploración superficial (rápida):**
```json
{
  "url": "https://ejemplo.com",
  "max_depth": 1,
  "max_pages": 10
}
```

**Exploración profunda:**
```json
{
  "url": "https://ejemplo.com",
  "max_depth": 4,
  "max_pages": 100
}
```

**Exploración móvil:**
```json
{
  "url": "https://ejemplo.com",
  "viewport": "mobile",
  "max_depth": 2,
  "max_pages": 50
}
```

---

## 📊 Resultados que Obtienes

```json
{
  "base_url": "https://ejemplo.com",
  "total_pages_visited": 25,
  "total_buttons_clicked": 47,
  "total_links_followed": 18,
  "total_ads_found": 12,
  "total_forms_found": 5,
  "sitemap": [
    "https://ejemplo.com",
    "https://ejemplo.com/productos",
    "https://ejemplo.com/contacto",
    ...
  ],
  "screenshots": [
    "path/to/screenshot1.png",
    "path/to/screenshot2.png",
    ...
  ]
}
```

---

## 🎯 Casos de Uso

### 1. **Verificar que anuncios funcionan**
Explora tu sitio para ver si tus anuncios (Google Ads, banners) se están mostrando y son clickeables.

### 2. **Testear como usuario real**
Simula cómo navegaría un visitante real, haciendo click en todo.

### 3. **Auditoría de UX**
Identifica todos los botones, formularios y elementos interactivos.

### 4. **Competencia**
Explora sitios de la competencia para ver su estructura y anuncios.

### 5. **QA automatizado**
Antes de lanzar, verifica que todos los enlaces, botones y formularios funcionen.

---

## 🔍 Qué Detecta Específicamente

### Anuncios:
- ✅ Google Ads (AdSense, AdWords)
- ✅ Facebook Ads
- ✅ Banners publicitarios
- ✅ Enlaces de afiliados (Amazon, ClickBank, etc.)
- ✅ iFrames de anuncios

### Botones:
- ✅ Botones HTML (`<button>`)
- ✅ Botones de submit
- ✅ CTAs (Call-to-Action)
- ✅ Enlaces con clase `btn` o `button`

### Formularios:
- ✅ Formularios de contacto
- ✅ Formularios de registro
- ✅ Formularios de newsletter
- ✅ Checkouts / Pagos

---

## ⚡ Tips

### Tiempo estimado:

| Páginas | Tiempo aproximado |
|---------|-------------------|
| 10 páginas | 1-2 minutos |
| 30 páginas | 3-5 minutos |
| 50 páginas | 5-8 minutos |
| 100 páginas | 10-15 minutos |

### Para exploración rápida:
```json
{
  "max_depth": 1,
  "max_pages": 10
}
```

### Para exploración completa:
```json
{
  "max_depth": 3,
  "max_pages": 100
}
```

---

## 🚨 Consideraciones

⚠️ **Respeta los términos de servicio** de los sitios que explores
⚠️ **No abuses** - Usa delays razonables entre requests
⚠️ **Sitios grandes** pueden tardar mucho - empieza con `max_pages` bajo
⚠️ **Anuncios de terceros** pueden abrir nuevas pestañas (el bot las cierra automáticamente)

---

## 📝 Ejemplo Completo

```bash
# 1. Activar entorno
cd backend
./venv/Scripts/activate

# 2. Explorar Amazon
python explore_demo.py https://amazon.com

# Resultado:
# ✅ EXPLORACIÓN COMPLETADA
# 📊 Estadísticas:
#   • Páginas visitadas: 30
#   • Botones encontrados: 85
#   • Enlaces seguidos: 25
#   • 📢 ANUNCIOS encontrados: 23
#   • Formularios detectados: 4
```

---

## 🆘 Problemas Comunes

**Error: "playwright not found"**
```bash
playwright install chromium
```

**Error: "timeout"**
- Aumenta el `BROWSER_TIMEOUT` en `.env`
- Reduce `max_pages` para sitios lentos

**No detecta anuncios**
- Algunos anuncios cargan con JavaScript después
- Prueba con `max_depth: 2` para darles tiempo

---

¿Listo para explorar? 🚀

```bash
python explore_demo.py https://tu-sitio.com
```
