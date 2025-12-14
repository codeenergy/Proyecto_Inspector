"""
Configuración de Escalado para TrafficBot Pro
Cambia fácilmente entre diferentes niveles de escalado
"""

# =============================================================================
# CONFIGURACIÓN DE ESCALADO
# =============================================================================

class ScalingConfig:
    """
    Configuraciones predefinidas para diferentes niveles de escalado
    """

    # Railway Hobby - Configuración Actual (Estable)
    HOBBY_STABLE = {
        'max_concurrent_sessions': 1,
        'max_targets_recommended': 12,
        'pageviews_per_target': 10,
        'estimated_daily_pageviews': 9000,
        'estimated_monthly_pageviews': 270000,
        'monetag_rpm': 3.00,  # Con geo-targeting optimizado
        'estimated_monthly_revenue': 810,
        'monthly_cost': 0,
        'net_profit': 810,
        'description': 'Configuración actual - Estable, sin riesgo de crash'
    }

    # Railway Hobby - Optimizado (2 sesiones)
    HOBBY_OPTIMIZED = {
        'max_concurrent_sessions': 2,
        'max_targets_recommended': 16,
        'pageviews_per_target': 10,
        'estimated_daily_pageviews': 19200,
        'estimated_monthly_pageviews': 576000,
        'monetag_rpm': 3.00,
        'estimated_monthly_revenue': 1728,
        'monthly_cost': 0,
        'net_profit': 1728,
        'description': 'Railway Hobby con optimizaciones de RAM - Requiere args de Playwright'
    }

    # Railway Pro - Para $5K/mes ⭐ RECOMENDADO
    PRO_5K = {
        'max_concurrent_sessions': 6,
        'max_targets_recommended': 24,
        'pageviews_per_target': 10,
        'estimated_daily_pageviews': 57600,
        'estimated_monthly_pageviews': 1728000,
        'monetag_rpm': 3.00,
        'estimated_monthly_revenue': 5184,
        'monthly_cost': 20,
        'net_profit': 5164,
        'description': 'Railway Pro - Objetivo $5K/mes alcanzado ✅'
    }

    # Hetzner VPS - Máximo Performance
    VPS_MAX = {
        'max_concurrent_sessions': 10,
        'max_targets_recommended': 40,
        'pageviews_per_target': 10,
        'estimated_daily_pageviews': 96000,
        'estimated_monthly_pageviews': 2880000,
        'monetag_rpm': 3.00,
        'estimated_monthly_revenue': 8640,
        'monthly_cost': 16,
        'net_profit': 8624,
        'description': 'Hetzner CPX31 - Performance máximo, mejor ROI'
    }


# =============================================================================
# CONFIGURACIÓN ACTIVA
# =============================================================================

# ⚠️ CAMBIA ESTA LÍNEA PARA ESCALAR:
ACTIVE_CONFIG = ScalingConfig.HOBBY_STABLE  # Actual: 1 sesión, estable

# Para escalar a 2 sesiones (gratis):
# ACTIVE_CONFIG = ScalingConfig.HOBBY_OPTIMIZED

# Para escalar a Railway Pro ($5K/mes):
# ACTIVE_CONFIG = ScalingConfig.PRO_5K

# Para máximo performance (Hetzner VPS):
# ACTIVE_CONFIG = ScalingConfig.VPS_MAX


# =============================================================================
# CONFIGURACIÓN DE MONETAG
# =============================================================================

class MonetTagConfig:
    """
    Configuración específica para optimización de Monetag
    """

    # RPM por geografía (Revenue per 1000 pageviews)
    RPM_BY_GEO = {
        'US': 4.00,
        'CA': 3.50,
        'UK': 3.00,
        'AU': 3.00,
        'DE': 2.50,
        'FR': 2.00,
        'ES': 1.50,
        'IT': 1.50,
        'MX': 0.80,
        'BR': 0.60,
        'IN': 0.30,
        'GLOBAL': 1.50,  # Promedio global sin optimización
    }

    # User agents premium (simula tráfico de alto valor)
    PREMIUM_USER_AGENTS = [
        # US Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # US Mac
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # Canada Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # UK Linux
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # Australia Mac
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    ]

    # Formatos de anuncios y sus RPM
    AD_FORMATS = {
        'popunder': {
            'rpm': 2.00,
            'weight': 0.65,  # 65% del revenue
            'description': 'Pop-under ads - Más rentable'
        },
        'push': {
            'rpm': 0.50,
            'weight': 0.20,  # 20% del revenue
            'description': 'Push notifications'
        },
        'native': {
            'rpm': 0.30,
            'weight': 0.15,  # 15% del revenue
            'description': 'Native banner ads'
        }
    }

    # RPM combinado esperado
    @classmethod
    def get_combined_rpm(cls):
        """Calcula RPM combinado de todos los formatos"""
        total = sum(
            format_data['rpm'] * format_data['weight']
            for format_data in cls.AD_FORMATS.values()
        )
        return round(total, 2)


# =============================================================================
# OPTIMIZACIONES DE PLAYWRIGHT
# =============================================================================

PLAYWRIGHT_OPTIMIZED_ARGS = [
    '--disable-blink-features=AutomationControlled',
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--disable-setuid-sandbox',

    # Optimizaciones de RAM para Monetag
    '--disable-gpu',              # Ahorra ~50MB RAM
    '--single-process',           # Ahorra ~100MB RAM (crítico)
    '--no-zygote',                # Ahorra ~30MB RAM
    '--disable-web-security',     # Permite cargar todos los anuncios
    '--disable-features=IsolateOrigins,site-per-process',  # Ahorra ~80MB RAM

    # Optimizaciones de performance
    '--disable-background-networking',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-breakpad',
    '--disable-client-side-phishing-detection',
    '--disable-component-update',
    '--disable-default-apps',
    '--disable-domain-reliability',
    '--disable-extensions',
    '--disable-features=AudioServiceOutOfProcess',
    '--disable-hang-monitor',
    '--disable-ipc-flooding-protection',
    '--disable-notifications',
    '--disable-offer-store-unmasked-wallet-cards',
    '--disable-popup-blocking',
    '--disable-print-preview',
    '--disable-prompt-on-repost',
    '--disable-renderer-backgrounding',
    '--disable-sync',
    '--disable-translate',
    '--metrics-recording-only',
    '--no-first-run',
    '--no-default-browser-check',
    '--safebrowsing-disable-auto-update',
    '--enable-automation',
    '--password-store=basic',
    '--use-mock-keychain',
]


# =============================================================================
# CALCULADORA DE REVENUE
# =============================================================================

def calculate_revenue(config=ACTIVE_CONFIG):
    """
    Calcula revenue estimado basado en configuración
    """
    monthly_pageviews = config['estimated_monthly_pageviews']
    rpm = config['monetag_rpm']
    monthly_revenue = (monthly_pageviews * rpm) / 1000
    monthly_cost = config['monthly_cost']
    net_profit = monthly_revenue - monthly_cost

    return {
        'monthly_pageviews': f"{monthly_pageviews:,}",
        'rpm': f"${rpm:.2f}",
        'gross_revenue': f"${monthly_revenue:,.2f}",
        'monthly_cost': f"${monthly_cost:.2f}",
        'net_profit': f"${net_profit:,.2f}",
        'roi': f"{(net_profit / monthly_cost * 100):.0f}%" if monthly_cost > 0 else "∞%",
    }


# =============================================================================
# IMPRIMIR CONFIGURACIÓN ACTUAL
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("📊 TRAFFICBOT PRO - CONFIGURACIÓN DE ESCALADO ACTIVA")
    print("="*70 + "\n")

    print(f"Nivel: {ACTIVE_CONFIG['description']}")
    print(f"Sesiones concurrentes: {ACTIVE_CONFIG['max_concurrent_sessions']}")
    print(f"Targets recomendados: {ACTIVE_CONFIG['max_targets_recommended']}")
    print(f"Pageviews por target: {ACTIVE_CONFIG['pageviews_per_target']}")
    print()

    print("💰 PROYECCIÓN DE REVENUE:")
    revenue = calculate_revenue()
    for key, value in revenue.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    print()
    print("📈 MONETAG RPM COMBINADO:")
    combined_rpm = MonetTagConfig.get_combined_rpm()
    print(f"  RPM esperado (multi-formato): ${combined_rpm:.2f}")

    print("\n" + "="*70)
    print("💡 Para cambiar de nivel, edita ACTIVE_CONFIG en SCALING_CONFIG.py")
    print("="*70 + "\n")
