"""
Simulador de Usuario con Undetected Chrome
Ultra sigiloso - Evade detección de Monetag y otros ad networks
"""
import asyncio
import random
import logging
from typing import Dict, List, Optional
from datetime import datetime
import time

# Undetected Chrome imports
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)


class UndetectedUserSimulator:
    """
    Simulador ultra sigiloso usando Undetected Chrome
    Evade detección de Monetag mejor que Playwright
    """

    def __init__(self):
        self.driver: Optional[uc.Chrome] = None
        self.popup_detected = False
        self.initial_window = None

    def setup_driver(self, viewport: Dict = None):
        """Inicializar navegador Undetected Chrome"""
        if viewport is None:
            viewport = {"width": 1920, "height": 1080}

        options = uc.ChromeOptions()

        # ULTRA STEALTH: Configuración para evitar detección
        options.add_argument(f'--window-size={viewport["width"]},{viewport["height"]}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')

        # User agent realista
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        options.add_argument(f'user-agent={random.choice(user_agents)}')

        # Preferencias adicionales
        prefs = {
            'profile.default_content_setting_values.notifications': 1,  # Permitir notificaciones
            'profile.managed_default_content_settings.popups': 1,  # Permitir pop-ups
        }
        options.add_experimental_option('prefs', prefs)

        logger.info("🚀 Iniciando Undetected Chrome...")
        self.driver = uc.Chrome(options=options, version_main=120)
        self.initial_window = self.driver.current_window_handle

        logger.info("✅ Undetected Chrome iniciado exitosamente")
        return self.driver

    def human_scroll(self, distance: int = None, steps: int = 5):
        """Scroll natural con paradas aleatorias"""
        if distance is None:
            # Scroll aleatorio entre 200-800px
            distance = random.randint(200, 800)

        step_size = distance // steps

        for i in range(steps):
            scroll_amount = step_size + random.randint(-20, 20)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.1, 0.3))

            # Pausa de lectura aleatoria
            if random.random() < 0.3:
                time.sleep(random.uniform(0.5, 1.5))

    def human_click(self, element):
        """Click con movimiento de mouse realista"""
        try:
            # Scroll al elemento
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(random.uniform(0.2, 0.5))

            # Movimiento de mouse con ActionChains
            actions = ActionChains(self.driver)

            # Mover a posición aleatoria cerca del elemento
            x_offset = random.randint(-10, 10)
            y_offset = random.randint(-10, 10)

            actions.move_to_element_with_offset(element, x_offset, y_offset)
            actions.pause(random.uniform(0.1, 0.3))
            actions.click()
            actions.perform()

            logger.info(f"💰 Click HUMANO realizado (offset: x={x_offset}, y={y_offset})")
            return True

        except Exception as e:
            logger.error(f"Error en click: {e}")
            return False

    def detect_monetag_scripts(self):
        """Detectar TODOS los scripts de Monetag en la página"""
        try:
            scripts = self.driver.execute_script("""
                const scripts = Array.from(document.querySelectorAll('script'));

                // TODOS los dominios conocidos de Monetag y ad networks
                const adDomains = [
                    'monetag', 'gizokraijaw', '3nbf4.com', 'nap5k.com',
                    'otieu.com', 'thubanoa.com', 'juicyads.com', 'propellerads',
                    'adsterra', 'popads', 'popcash', 'admaven', 'clickadu',
                    'exoclick', 'hilltopads', 'bidvertiser', 'revcontent'
                ];

                const adScripts = scripts.filter(s => {
                    if (s.dataset.zone) return true;
                    if (s.src) {
                        return adDomains.some(domain => s.src.includes(domain));
                    }
                    return false;
                });

                return adScripts.map(s => ({
                    src: s.src || 'inline',
                    zone: s.dataset.zone || 'N/A',
                    async: s.async,
                    defer: s.defer
                }));
            """)

            if scripts and len(scripts) > 0:
                logger.info(f"✅ Scripts detectados: {len(scripts)} scripts")
                for i, script in enumerate(scripts):
                    src = script['src'][:60] + '...' if len(script['src']) > 60 else script['src']
                    zone = script['zone']
                    logger.info(f"   [{i+1}] Zone: {zone} | {src}")
            else:
                logger.warning("⚠️ NO se detectaron scripts de ads en la página")

            return scripts

        except Exception as e:
            logger.error(f"Error detectando scripts: {e}")
            return []

    def detect_popups(self):
        """Detectar pop-unders y nuevas ventanas"""
        try:
            all_windows = self.driver.window_handles

            if len(all_windows) > 1:
                logger.info(f"🎯 POP-UNDER DETECTADO! Total ventanas: {len(all_windows)}")
                self.popup_detected = True

                # Cerrar ventanas extra (pop-unders)
                for window in all_windows:
                    if window != self.initial_window:
                        self.driver.switch_to.window(window)
                        logger.info(f"   → Cerrando pop-under: {self.driver.title[:50]}")
                        self.driver.close()

                # Volver a ventana principal
                self.driver.switch_to.window(self.initial_window)
                return True

            return False

        except Exception as e:
            logger.error(f"Error detectando popups: {e}")
            return False

    async def run_session(self, config: Dict):
        """Ejecutar sesión completa de tráfico"""
        url = config.get("url")
        target_pageviews = config.get("target_pageviews", 8)
        ad_click_probability = config.get("ad_click_probability", 0.65)
        viewport = config.get("viewport", {"width": 1920, "height": 1080})

        logger.info(f"▶️ Iniciando sesión UNDETECTED para: {url}")

        stats = {
            "pages_visited": 0,
            "ads_clicked": 0,
            "popups_detected": 0
        }

        try:
            # Iniciar navegador
            self.setup_driver(viewport)

            # Navegar a la URL
            logger.info(f"🌐 Navegando a {url}")
            self.driver.get(url)

            # Esperar carga completa
            time.sleep(random.uniform(3, 5))

            # Limpiar sessionStorage para vignette
            self.driver.execute_script("sessionStorage.clear();")
            logger.info("🧹 SessionStorage limpiado para permitir Vignette")

            # Detectar scripts de Monetag
            scripts = self.detect_monetag_scripts()

            # Esperar 15 segundos para que scripts de Monetag se inicialicen
            logger.info("⏳ Esperando 15s para inicialización de scripts Monetag...")
            time.sleep(15)

            # Visitar páginas
            for page_num in range(target_pageviews):
                logger.info(f"📄 Página #{page_num + 1}/{target_pageviews}")

                # Scroll natural
                self.human_scroll()
                time.sleep(random.uniform(2, 4))

                # Click con probabilidad para activar ads
                if random.random() < ad_click_probability:
                    try:
                        # Buscar elementos clickeables
                        safe_selectors = ['main h1', 'main h2', 'main p', 'article', 'main div']

                        for selector in safe_selectors:
                            try:
                                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                                if elements:
                                    element = random.choice(elements[:5] if len(elements) > 5 else elements)

                                    # Detectar popups ANTES del click
                                    windows_before = len(self.driver.window_handles)

                                    # Click humano
                                    if self.human_click(element):
                                        time.sleep(random.uniform(0.5, 1.0))

                                        # Detectar popups DESPUÉS del click
                                        if self.detect_popups():
                                            stats["ads_clicked"] += 1
                                            stats["popups_detected"] += 1
                                        else:
                                            logger.warning("⚠️ Click realizado pero no se detectó pop-under")

                                        break

                            except (NoSuchElementException, TimeoutException):
                                continue

                    except Exception as e:
                        logger.error(f"Error en click: {e}")

                stats["pages_visited"] += 1

                # Navegar a siguiente página o home
                if page_num < target_pageviews - 1:
                    try:
                        # Buscar links internos
                        links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href^="/"], a[href*="' + url + '"]')
                        if links:
                            link = random.choice(links[:10] if len(links) > 10 else links)
                            self.human_click(link)
                            time.sleep(random.uniform(2, 4))
                        else:
                            # Volver al home
                            self.driver.get(url)
                            time.sleep(random.uniform(2, 3))
                    except:
                        self.driver.get(url)
                        time.sleep(random.uniform(2, 3))

            logger.info(f"✅ Sesión completada: {stats}")
            return {
                "success": True,
                "stats": stats,
                "log": [f"Páginas visitadas: {stats['pages_visited']}", f"Ads clickeados: {stats['ads_clicked']}"]
            }

        except Exception as e:
            logger.error(f"❌ Error en sesión: {e}")
            return {
                "success": False,
                "stats": stats,
                "log": [str(e)]
            }

        finally:
            if self.driver:
                logger.info("🧹 Cerrando navegador...")
                self.driver.quit()


# Función wrapper async para compatibilidad
async def run_undetected_session(config: Dict):
    """Wrapper async para ejecutar sesión con Undetected Chrome"""
    simulator = UndetectedUserSimulator()
    return await simulator.run_session(config)
