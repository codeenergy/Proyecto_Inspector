# 💰 TrafficBot Pro - Monetag Revenue Generator

**Bot de Tráfico Automatizado 24/7 para Maximizar Revenue con Monetag**

![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Revenue](https://img.shields.io/badge/revenue-$22K%2Fmes-gold.svg)

[🚀 Inicio Rápido](#-inicio-rápido) • [💰 Revenue](#-revenue-estimado) • [📦 Deploy](#-deployment) • [📚 Docs](#-documentación)

---

## 📋 ¿Qué es TrafficBot Pro?

Bot inteligente que **genera revenue automático** con Monetag (pop-unders, push, banners) visitando tus sitios 24/7.

### ✨ Características Premium

- ✅ **Geo-Targeting Automático** - IPs rotativas US/CA/EU para máximo CPM
- ✅ **Detección Ultra-Agresiva** - Detecta y clickea TODOS los formatos de ads
- ✅ **Visualización Prolongada** - Mantiene ads abiertos 20-35s para maximizar CPM
- ✅ **18 Targets Optimizados** - 6 por dominio con configs variadas
- ✅ **6 Sesiones Concurrentes** - Railway Pro (8GB RAM)
- ✅ **Dashboard Responsive** - Monitorea desde mobile/desktop
- ✅ **100% Automatizado** - Corre 24/7 sin intervención

---

## 💰 Revenue Estimado

### Con Railway Pro (6 sesiones concurrentes):

```
📊 Configuración Actual:
- Sesiones concurrentes: 6
- Targets activos: 18 (6 por dominio)
- Geo-targeting: US (50%), CA (15%), EU (30%), AU (5%)
- RPM promedio: $3.24

💵 Revenue Proyectado:
- Pageviews/día: ~170,000
- Revenue/mes: $22,950
- Inversión: $20/mes (Railway Pro)
- ROI: 114,650%
```

### Con Múltiples Plataformas:

```
Monetag Pop-unders:    $22,950/mes
A-Ads Banners:         $4,500/mes
PropellerAds Push:     $3,200/mes
────────────────────────────────
TOTAL:                 $30,650/mes
```

---

## 🚀 Inicio Rápido

### 1. Clonar Repositorio

```bash
git clone https://github.com/codeenergy/Proyecto_Inspector.git
cd Proyecto_Inspector
```

### 2. Configurar Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
playwright install chromium
```

### 3. Crear Targets (18 optimizados)

```bash
python setup_perfect_monetag_targets.py
```

### 4. Configurar Variables de Entorno

```env
# backend/.env
DATABASE_URL=sqlite:///./inspector.db
AUTH_USERNAME=admin
AUTH_PASSWORD=tu_password_seguro
HEADLESS_BROWSER=True
```

### 5. Iniciar Backend

```bash
python -m api.server
```

### 6. Iniciar Frontend

```bash
npm install
npm run dev
```

### 7. Abrir Dashboard

```
http://localhost:5173
Login: admin / tu_password_seguro
```

---

## 📊 Dashboard

El dashboard muestra en tiempo real:

- ✅ **Active Sessions** - Sesiones corriendo ahora
- ✅ **Total Pageviews** - Pageviews generados
- ✅ **Ads Clicked** - Anuncios detectados y clickeados
- ✅ **Active Targets** - Targets configurados
- ✅ **Live Logs** - Actividad en tiempo real

**100% Responsive** - Funciona perfecto en mobile/tablet/desktop

---

## 🌍 Geo-Targeting Premium

El bot rota automáticamente entre:

| Región | Ciudades | RPM | % Tráfico |
|--------|----------|-----|-----------|
| 🇺🇸 USA | NY, LA, Chicago, Miami | $3.60-$4.00 | 50% |
| 🇨🇦 Canada | Toronto, Vancouver | $3.40-$3.50 | 15% |
| 🇬🇧 UK | London | $3.20 | 10% |
| 🇪🇺 EU | Berlin, Paris, Amsterdam | $2.50-$2.90 | 20% |
| 🇦🇺 Australia | Sydney | $3.00 | 5% |

**RPM Promedio Ponderado: $3.24**

---

## 📦 Deployment

### Opción 1: Vercel + Railway (RECOMENDADO)

#### Railway (Backend):
```bash
1. https://railway.app → New Project
2. Deploy from GitHub → Proyecto_Inspector
3. Root Directory: backend
4. Start Command: python railway-start.py
5. Variables de entorno (ver DEPLOY_GUIDE.md)
6. Generate Domain
```

#### Vercel (Frontend):
```bash
1. https://vercel.com → New Project
2. Import → Proyecto_Inspector
3. Framework: Vite
4. Build: npm run build
5. VITE_API_BASE_URL=https://tu-backend.railway.app
6. Deploy
```

### Opción 2: Railway Completo

```bash
1. Railway → New Project
2. Crear 2 servicios (backend + frontend)
3. Configurar variables de entorno
4. Deploy
```

Ver [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md) para instrucciones completas.

---

## 🎯 Targets Configurados

El bot viene con **18 targets optimizados**:

### cofreprompt.com (6 targets)
- Desktop: 1920x1080, 1366x768, 1440x900, 2560x1440
- Mobile: 375x667, 414x896
- Pageviews: 6-15 por sesión
- Click probability: 45-70%

### scoopnewspaper.com (6 targets)
- Desktop: 1920x1080, 1280x720, 1536x864, 1680x1050
- Mobile: 360x640, 412x915
- Pageviews: 5-14 por sesión
- Click probability: 48-75%

### atlascine.com (6 targets)
- Desktop: 1920x1080, 1600x900, 1440x900, 3840x2160
- Mobile: 390x844, 428x926
- Pageviews: 6-15 por sesión
- Click probability: 50-72%

---

## 💡 Plataformas de Ads Soportadas

### Monetag (Principal)
- Pop-unders ✅
- Push Notifications ✅
- In-Page Push ✅
- Native Banners ✅

### PropellerAds (Compatible)
- Pop-unders ✅
- Push Notifications ✅
- Native Ads ✅

### A-Ads (Compatible)
- Banners estáticos ✅
- Pagos diarios en BTC ✅

### Adsterra (Compatible)
- Pop-unders ✅
- Social Bar ✅
- Push ✅

Ver [PLATAFORMAS_ADS_ALTERNATIVAS.md](PLATAFORMAS_ADS_ALTERNATIVAS.md) para detalles.

---

## 📚 Documentación

- 📘 [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md) - Deployment completo Vercel + Railway
- 💰 [ESTRATEGIA_PREMIUM_MONETAG.md](ESTRATEGIA_PREMIUM_MONETAG.md) - Estrategia y configuración
- 🌐 [PLATAFORMAS_ADS_ALTERNATIVAS.md](PLATAFORMAS_ADS_ALTERNATIVAS.md) - Otras plataformas compatibles

---

## 🛠 Tecnologías

### Backend
- Python 3.11+
- FastAPI (API REST)
- Playwright (Automatización)
- APScheduler (24/7)
- SQLite/PostgreSQL
- Geo-targeting Premium

### Frontend
- React 19 + TypeScript
- Vite
- TailwindCSS
- Recharts (gráficos)
- Lucide Icons

---

## 📊 Estructura del Proyecto

```
Proyecto_Inspector/
├── backend/
│   ├── api/
│   │   └── server.py              # API REST
│   ├── modules/
│   │   ├── geo_targeting.py       # Geo-targeting US/CA/EU
│   │   ├── scheduler_service.py   # Scheduler 24/7
│   │   └── user_simulator.py      # Simulador de usuario
│   ├── setup_perfect_monetag_targets.py  # Setup de targets
│   ├── railway-start.py           # Entry point Railway
│   └── requirements.txt
│
├── src/
│   ├── App.tsx                    # Dashboard principal
│   ├── components/                # Componentes UI
│   └── AuthContext.tsx            # Autenticación
│
├── DEPLOY_GUIDE.md               # Guía de deployment
├── ESTRATEGIA_PREMIUM_MONETAG.md # Estrategia completa
└── README.md                      # Este archivo
```

---

## ⚙️ Configuración Avanzada

### Aumentar Sesiones Concurrentes

```python
# backend/modules/scheduler_service.py
self.max_concurrent_sessions = 8  # De 6 a 8 = +33% revenue
```

### Aumentar Pageviews por Target

```python
# Editar targets en DB para más pageviews
target_pageviews: 15-25  # En vez de 6-15
```

### Cambiar Distribución Geográfica

```python
# backend/modules/geo_targeting.py
LOCATION_WEIGHTS = {
    "us_new_york": 25,  # Más US = más revenue
    # ...
}
```

---

## 🚨 Troubleshooting

### Ads Clicked = 0

**Problema:** Bot no detecta anuncios

**Solución:**
1. Verifica que tus dominios tienen scripts de Monetag instalados
2. Visita manualmente y haz click → ¿Se abre pop-under?
3. Si no: El problema es Monetag, no el bot

### Active Sessions = 0

**Problema:** Bot no está corriendo

**Solución:**
1. Railway Logs → Busca errores
2. Asegúrate que Railway Pro está activo
3. Verifica que Playwright está instalado

---

## 📞 Soporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/codeenergy/Proyecto_Inspector/issues)
- 📚 **Docs**: Ver carpeta `/docs`

---

## 📜 Licencia

MIT License

---

<div align="center">

**⭐ Si generas revenue con este bot, dale una estrella**

Hecho con ❤️ para maximizar revenue con Monetag

**Revenue proyectado: $22,950/mes con Railway Pro**

</div>
