"""
Sistema de Geo-Targeting Premium para Maximizar CPM
====================================================
Rota entre localizaciones de alto valor: US, Canadá, Europa
Configura User-Agent, timezone, idioma, geolocalización para cada sesión
"""
import random
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class GeoTargeting:
    """
    Sistema de geo-targeting para simular tráfico premium de alto valor
    """

    # =============================================================================
    # TIER 1 GEOLOCATIONS - ALTO CPM ($2.50 - $4.00 RPM)
    # =============================================================================

    PREMIUM_LOCATIONS = {
        # ========== UNITED STATES (CPM más alto) ==========
        "us_new_york": {
            "country": "US",
            "country_code": "us",
            "city": "New York",
            "timezone": "America/New_York",
            "locale": "en-US",
            "languages": ["en-US", "en"],
            "geolocation": {"latitude": 40.7128, "longitude": -74.0060},
            "currency": "USD",
            "rpm": 4.00,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            ]
        },
        "us_los_angeles": {
            "country": "US",
            "country_code": "us",
            "city": "Los Angeles",
            "timezone": "America/Los_Angeles",
            "locale": "en-US",
            "languages": ["en-US", "en", "es-US"],
            "geolocation": {"latitude": 34.0522, "longitude": -118.2437},
            "currency": "USD",
            "rpm": 3.80,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            ]
        },
        "us_chicago": {
            "country": "US",
            "country_code": "us",
            "city": "Chicago",
            "timezone": "America/Chicago",
            "locale": "en-US",
            "languages": ["en-US", "en"],
            "geolocation": {"latitude": 41.8781, "longitude": -87.6298},
            "currency": "USD",
            "rpm": 3.70,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ]
        },
        "us_miami": {
            "country": "US",
            "country_code": "us",
            "city": "Miami",
            "timezone": "America/New_York",
            "locale": "en-US",
            "languages": ["en-US", "en", "es-US"],
            "geolocation": {"latitude": 25.7617, "longitude": -80.1918},
            "currency": "USD",
            "rpm": 3.60,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ]
        },

        # ========== CANADA (Alto CPM) ==========
        "ca_toronto": {
            "country": "Canada",
            "country_code": "ca",
            "city": "Toronto",
            "timezone": "America/Toronto",
            "locale": "en-CA",
            "languages": ["en-CA", "en", "fr-CA"],
            "geolocation": {"latitude": 43.6532, "longitude": -79.3832},
            "currency": "CAD",
            "rpm": 3.50,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ]
        },
        "ca_vancouver": {
            "country": "Canada",
            "country_code": "ca",
            "city": "Vancouver",
            "timezone": "America/Vancouver",
            "locale": "en-CA",
            "languages": ["en-CA", "en"],
            "geolocation": {"latitude": 49.2827, "longitude": -123.1207},
            "currency": "CAD",
            "rpm": 3.40,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ]
        },

        # ========== UNITED KINGDOM ==========
        "uk_london": {
            "country": "United Kingdom",
            "country_code": "uk",
            "city": "London",
            "timezone": "Europe/London",
            "locale": "en-GB",
            "languages": ["en-GB", "en"],
            "geolocation": {"latitude": 51.5074, "longitude": -0.1278},
            "currency": "GBP",
            "rpm": 3.20,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ]
        },

        # ========== GERMANY ==========
        "de_berlin": {
            "country": "Germany",
            "country_code": "de",
            "city": "Berlin",
            "timezone": "Europe/Berlin",
            "locale": "de-DE",
            "languages": ["de-DE", "de", "en"],
            "geolocation": {"latitude": 52.5200, "longitude": 13.4050},
            "currency": "EUR",
            "rpm": 2.80,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ]
        },
        "de_munich": {
            "country": "Germany",
            "country_code": "de",
            "city": "Munich",
            "timezone": "Europe/Berlin",
            "locale": "de-DE",
            "languages": ["de-DE", "de", "en"],
            "geolocation": {"latitude": 48.1351, "longitude": 11.5820},
            "currency": "EUR",
            "rpm": 2.70,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ]
        },

        # ========== FRANCE ==========
        "fr_paris": {
            "country": "France",
            "country_code": "fr",
            "city": "Paris",
            "timezone": "Europe/Paris",
            "locale": "fr-FR",
            "languages": ["fr-FR", "fr", "en"],
            "geolocation": {"latitude": 48.8566, "longitude": 2.3522},
            "currency": "EUR",
            "rpm": 2.50,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ]
        },

        # ========== NETHERLANDS ==========
        "nl_amsterdam": {
            "country": "Netherlands",
            "country_code": "nl",
            "city": "Amsterdam",
            "timezone": "Europe/Amsterdam",
            "locale": "nl-NL",
            "languages": ["nl-NL", "nl", "en"],
            "geolocation": {"latitude": 52.3676, "longitude": 4.9041},
            "currency": "EUR",
            "rpm": 2.90,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ]
        },

        # ========== SPAIN ==========
        "es_madrid": {
            "country": "Spain",
            "country_code": "es",
            "city": "Madrid",
            "timezone": "Europe/Madrid",
            "locale": "es-ES",
            "languages": ["es-ES", "es", "en"],
            "geolocation": {"latitude": 40.4168, "longitude": -3.7038},
            "currency": "EUR",
            "rpm": 2.30,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ]
        },

        # ========== AUSTRALIA (Bonus Tier 1) ==========
        "au_sydney": {
            "country": "Australia",
            "country_code": "au",
            "city": "Sydney",
            "timezone": "Australia/Sydney",
            "locale": "en-AU",
            "languages": ["en-AU", "en"],
            "geolocation": {"latitude": -33.8688, "longitude": 151.2093},
            "currency": "AUD",
            "rpm": 3.00,
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ]
        },
    }

    # Pesos para distribución realista (más tráfico de US/CA)
    LOCATION_WEIGHTS = {
        # US: 50% del tráfico
        "us_new_york": 15,
        "us_los_angeles": 15,
        "us_chicago": 10,
        "us_miami": 10,

        # Canada: 15% del tráfico
        "ca_toronto": 8,
        "ca_vancouver": 7,

        # UK: 10% del tráfico
        "uk_london": 10,

        # EU: 20% del tráfico
        "de_berlin": 6,
        "de_munich": 4,
        "fr_paris": 5,
        "nl_amsterdam": 3,
        "es_madrid": 2,

        # AU: 5% del tráfico
        "au_sydney": 5,
    }

    @classmethod
    def get_random_location(cls) -> Tuple[str, Dict]:
        """
        Obtener una ubicación aleatoria basada en pesos (más US/CA, menos EU)
        Returns: (location_key, location_data)
        """
        locations = list(cls.LOCATION_WEIGHTS.keys())
        weights = list(cls.LOCATION_WEIGHTS.values())

        location_key = random.choices(locations, weights=weights, k=1)[0]
        location_data = cls.PREMIUM_LOCATIONS[location_key]

        return location_key, location_data

    @classmethod
    def get_browser_config(cls, location_data: Dict, viewport_type: str = "desktop") -> Dict:
        """
        Generar configuración completa del navegador para una ubicación
        """
        # Seleccionar user agent aleatorio
        user_agent = random.choice(location_data["user_agents"])

        # Viewports según device
        viewports = {
            "desktop": [
                {"width": 1920, "height": 1080},
                {"width": 1366, "height": 768},
                {"width": 1440, "height": 900},
                {"width": 1536, "height": 864},
                {"width": 1600, "height": 900},
            ],
            "mobile": [
                {"width": 375, "height": 667},  # iPhone 8
                {"width": 414, "height": 896},  # iPhone 11/XR
                {"width": 390, "height": 844},  # iPhone 12/13
                {"width": 428, "height": 926},  # iPhone 13 Pro Max
                {"width": 360, "height": 640},  # Android común
            ]
        }

        # Detectar mobile en user agent
        is_mobile = "iPhone" in user_agent or "Android" in user_agent
        viewport = random.choice(viewports["mobile" if is_mobile else "desktop"])

        config = {
            "user_agent": user_agent,
            "viewport": viewport,
            "timezone": location_data["timezone"],
            "locale": location_data["locale"],
            "languages": location_data["languages"],
            "geolocation": location_data["geolocation"],
            "country": location_data["country"],
            "city": location_data["city"],
            "country_code": location_data["country_code"],
            "is_mobile": is_mobile,
            "has_touch": is_mobile,
        }

        logger.info(
            f"🌍 Geo-Target: {location_data['city']}, {location_data['country']} "
            f"(RPM: ${location_data['rpm']:.2f}) - "
            f"{'Mobile' if is_mobile else 'Desktop'} {viewport['width']}x{viewport['height']}"
        )

        return config

    @classmethod
    def get_high_cpm_referrers(cls) -> list:
        """
        Obtener referrers de alto valor para maximizar CPM
        """
        return [
            "https://www.google.com/",
            "https://www.facebook.com/",
            "https://t.co/",  # Twitter
            "https://www.linkedin.com/",
            "https://www.reddit.com/",
            "https://news.google.com/",
            "https://www.bing.com/",
            "https://duckduckgo.com/",
        ]

    @classmethod
    def calculate_weighted_rpm(cls) -> float:
        """
        Calcular RPM promedio ponderado según distribución de tráfico
        """
        total_weight = sum(cls.LOCATION_WEIGHTS.values())
        weighted_rpm = 0

        for location_key, weight in cls.LOCATION_WEIGHTS.items():
            location_rpm = cls.PREMIUM_LOCATIONS[location_key]["rpm"]
            weighted_rpm += (location_rpm * weight) / total_weight

        return round(weighted_rpm, 2)


# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def get_random_premium_location() -> Tuple[str, Dict]:
    """Helper para obtener ubicación premium aleatoria"""
    return GeoTargeting.get_random_location()


def get_premium_browser_config(viewport_type: str = "desktop") -> Dict:
    """
    Helper para obtener configuración completa del navegador con geo-targeting
    """
    location_key, location_data = GeoTargeting.get_random_location()
    return GeoTargeting.get_browser_config(location_data, viewport_type)


if __name__ == "__main__":
    # Test
    print("\n" + "="*80)
    print("GEO-TARGETING PREMIUM - TEST")
    print("="*80)

    print(f"\nRPM Promedio Ponderado: ${GeoTargeting.calculate_weighted_rpm():.2f}")

    print("\n10 Ubicaciones Aleatorias:")
    for i in range(10):
        location_key, location_data = get_random_premium_location()
        print(f"  {i+1}. {location_data['city']}, {location_data['country']} (RPM: ${location_data['rpm']:.2f})")

    print("\n3 Configuraciones de Navegador:")
    for i in range(3):
        config = get_premium_browser_config()
        print(f"\n  {i+1}. {config['city']}, {config['country']}")
        print(f"     User-Agent: {config['user_agent'][:60]}...")
        print(f"     Viewport: {config['viewport']}")
        print(f"     Timezone: {config['timezone']}")

    print("\n" + "="*80)
