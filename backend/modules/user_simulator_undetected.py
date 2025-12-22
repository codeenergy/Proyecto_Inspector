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

        logger.info("🚀 Iniciando Undetected Chrome...")

        try:
            # Crear opciones manualmente
            options = uc.ChromeOptions()

            # Configuración básica
            options.add_argument(f'--window-size={viewport["width"]},{viewport["height"]}')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')

            # NO headless para evitar detección
            options.headless = False

            # Permitir popups
            prefs = {
                'profile.default_content_setting_values.notifications': 1,
                'profile.managed_default_content_settings.popups': 1,
            }
            options.add_experimental_option('prefs', prefs)

            # Crear driver con opciones
            self.driver = uc.Chrome(options=options, driver_executable_path=None)

        except Exception as e:
            logger.error(f"Error iniciando Chrome: {e}")
            # Fallback: intentar sin opciones
            logger.info("Intentando fallback sin opciones...")
            self.driver = uc.Chrome()
            self.driver.set_window_size(viewport["width"], viewport["height"])

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

    def find_all_buttons(self):
        """Encontrar TODOS los botones en la página"""
        try:
            buttons = self.driver.execute_script("""
                // Buscar todos los elementos clickeables
                const selectors = [
                    'button',
                    'a[href]',
                    '[role="button"]',
                    'input[type="button"]',
                    'input[type="submit"]',
                    '[onclick]',
                    '.btn',
                    '.button'
                ];

                const allButtons = [];
                selectors.forEach(selector => {
                    document.querySelectorAll(selector).forEach(el => {
                        // Verificar que sea visible
                        const rect = el.getBoundingClientRect();
                        if (rect.width > 0 && rect.height > 0) {
                            allButtons.push({
                                tag: el.tagName,
                                text: el.innerText?.substring(0, 50) || el.value || 'Sin texto',
                                href: el.href || null,
                                visible: true
                            });
                        }
                    });
                });

                return allButtons;
            """)

            logger.info(f"🔘 Botones encontrados: {len(buttons)}")
            return buttons

        except Exception as e:
            logger.error(f"Error buscando botones: {e}")
            return []

    def detect_monetag_links(self):
        """Detectar enlaces de Monetag (Direct links)"""
        try:
            monetag_links = self.driver.execute_script("""
                const links = Array.from(document.querySelectorAll('a[href]'));

                // Dominios de Monetag conocidos
                const monetagDomains = [
                    'monetag', 'gizokraijaw', '3nbf4.com', 'nap5k.com',
                    'otieu.com', 'thubanoa.com'
                ];

                return links
                    .filter(link => monetagDomains.some(domain => link.href.includes(domain)))
                    .map(link => ({
                        href: link.href,
                        text: link.innerText?.substring(0, 30) || 'Sin texto'
                    }));
            """)

            if monetag_links and len(monetag_links) > 0:
                logger.info(f"💰 Enlaces de Monetag encontrados: {len(monetag_links)}")

            return monetag_links

        except Exception as e:
            logger.error(f"Error detectando enlaces Monetag: {e}")
            return []

    def handle_new_windows(self, wait_time: tuple = (3, 6)):
        """Manejar nuevas ventanas/pestañas como usuario normal"""
        try:
            all_windows = self.driver.window_handles

            if len(all_windows) > 1:
                new_windows_count = len(all_windows) - 1
                logger.info(f"🎯 {new_windows_count} ventana(s) nueva(s) detectada(s)")

                # Procesar cada ventana nueva
                for window in all_windows:
                    if window != self.initial_window:
                        self.driver.switch_to.window(window)
                        current_url = self.driver.current_url

                        logger.info(f"   📱 Ventana nueva: {current_url[:60]}...")

                        # Esperar como usuario normal leyendo
                        wait = random.uniform(wait_time[0], wait_time[1])
                        logger.info(f"   ⏳ Esperando {wait:.1f}s (comportamiento humano)...")
                        time.sleep(wait)

                        # Scroll rápido en la ventana nueva
                        try:
                            self.human_scroll(distance=300, steps=3)
                        except:
                            pass

                        logger.info(f"   ✅ Cerrando ventana")
                        self.driver.close()

                # Volver a ventana principal
                self.driver.switch_to.window(self.initial_window)
                logger.info(f"   🔙 Volviendo a ventana principal")
                return new_windows_count

            return 0

        except Exception as e:
            logger.error(f"Error manejando ventanas: {e}")
            # Intentar volver a la ventana principal
            try:
                self.driver.switch_to.window(self.initial_window)
            except:
                pass
            return 0

    def click_all_buttons(self):
        """Hacer clic en TODOS los botones como usuario normal"""
        clicked_count = 0
        windows_opened = 0

        try:
            # Buscar todos los botones visibles
            buttons_selectors = [
                'button:not([style*="display: none"])',
                'a[href]:not([style*="display: none"])',
                '[role="button"]',
                'input[type="button"]',
                'input[type="submit"]',
                '.btn',
                '.button'
            ]

            for selector in buttons_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    logger.info(f"🔍 Selector '{selector}': {len(elements)} elementos")

                    # Hacer clic en cada elemento
                    for i, element in enumerate(elements[:10]):  # Limitar a 10 por selector
                        try:
                            # Verificar si es visible
                            if not element.is_displayed():
                                continue

                            # Guardar número de ventanas antes del click
                            windows_before = len(self.driver.window_handles)

                            # Click humano
                            text = element.text[:30] if element.text else "Sin texto"
                            logger.info(f"   🖱️ Clickeando botón {i+1}: '{text}'")

                            if self.human_click(element):
                                clicked_count += 1

                                # Esperar a que se abran nuevas ventanas
                                time.sleep(random.uniform(0.5, 1.0))

                                # Verificar si se abrieron nuevas ventanas
                                windows_after = len(self.driver.window_handles)
                                if windows_after > windows_before:
                                    new_windows = self.handle_new_windows()
                                    windows_opened += new_windows

                                # Esperar entre clicks
                                time.sleep(random.uniform(1.0, 2.0))

                        except Exception as e:
                            logger.debug(f"   ⚠️ Error en elemento: {str(e)[:50]}")
                            continue

                except Exception as e:
                    logger.debug(f"⚠️ Error con selector {selector}: {str(e)[:50]}")
                    continue

            logger.info(f"✅ Clicks completados: {clicked_count} botones | {windows_opened} ventanas abiertas")
            return clicked_count, windows_opened

        except Exception as e:
            logger.error(f"❌ Error haciendo clicks: {e}")
            return clicked_count, windows_opened

    async def run_session(self, config: Dict):
        """Ejecutar sesión completa de tráfico - MODO USUARIO NORMAL"""
        url = config.get("url")
        target_pageviews = config.get("target_pageviews", 8)
        viewport = config.get("viewport", {"width": 1920, "height": 1080})

        logger.info(f"▶️ Iniciando sesión MODO USUARIO NORMAL para: {url}")
        logger.info(f"   🎯 Objetivo: Hacer clic en TODOS los botones como usuario real")

        stats = {
            "pages_visited": 0,
            "buttons_clicked": 0,
            "windows_opened": 0
        }

        try:
            # Iniciar navegador
            self.setup_driver(viewport)

            # Navegar a la URL
            logger.info(f"🌐 Navegando a {url}")
            self.driver.get(url)

            # Esperar carga completa
            wait_time = random.uniform(4, 7)
            logger.info(f"⏳ Esperando {wait_time:.1f}s para carga completa...")
            time.sleep(wait_time)

            # Limpiar sessionStorage
            self.driver.execute_script("sessionStorage.clear();")
            logger.info("🧹 SessionStorage limpiado")

            # Visitar páginas
            for page_num in range(target_pageviews):
                logger.info(f"\n{'='*60}")
                logger.info(f"📄 Página #{page_num + 1}/{target_pageviews}")
                logger.info(f"{'='*60}")

                # Scroll natural para ver la página
                logger.info("📜 Scrolleando como usuario normal...")
                self.human_scroll(distance=random.randint(400, 800))
                time.sleep(random.uniform(2, 4))

                # HACER CLIC EN TODOS LOS BOTONES
                logger.info("\n🔘 Buscando y clickeando TODOS los botones...")
                buttons_clicked, windows_opened = self.click_all_buttons()

                stats["buttons_clicked"] += buttons_clicked
                stats["windows_opened"] += windows_opened
                stats["pages_visited"] += 1

                logger.info(f"\n📊 Stats de esta página:")
                logger.info(f"   🖱️ Botones clickeados: {buttons_clicked}")
                logger.info(f"   📱 Ventanas abiertas: {windows_opened}")

                # Navegar a siguiente página
                if page_num < target_pageviews - 1:
                    logger.info(f"\n🔄 Navegando a siguiente página...")

                    try:
                        # Buscar links internos
                        links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href^="/"], a[href*="' + url + '"]')

                        # Filtrar links de navegación (no Monetag)
                        internal_links = []
                        for link in links:
                            try:
                                href = link.get_attribute('href')
                                # Excluir enlaces de Monetag
                                if href and not any(domain in href for domain in ['monetag', 'gizokraijaw', '3nbf4', 'nap5k', 'otieu', 'thubanoa']):
                                    internal_links.append(link)
                            except:
                                continue

                        if internal_links:
                            link = random.choice(internal_links[:15])
                            logger.info(f"   🔗 Navegando a: {link.get_attribute('href')[:60]}")
                            self.human_click(link)
                            time.sleep(random.uniform(3, 5))
                        else:
                            # Volver al home
                            logger.info(f"   🏠 Volviendo al home")
                            self.driver.get(url)
                            time.sleep(random.uniform(3, 5))

                    except Exception as e:
                        logger.warning(f"   ⚠️ Error navegando, volviendo al home: {e}")
                        self.driver.get(url)
                        time.sleep(random.uniform(3, 5))

            logger.info(f"\n{'='*60}")
            logger.info(f"✅ SESIÓN COMPLETADA")
            logger.info(f"{'='*60}")
            logger.info(f"📊 Estadísticas finales:")
            logger.info(f"   📄 Páginas visitadas: {stats['pages_visited']}")
            logger.info(f"   🖱️ Botones clickeados: {stats['buttons_clicked']}")
            logger.info(f"   📱 Ventanas abiertas: {stats['windows_opened']}")
            logger.info(f"{'='*60}\n")

            return {
                "success": True,
                "stats": stats,
                "log": [
                    f"Páginas visitadas: {stats['pages_visited']}",
                    f"Botones clickeados: {stats['buttons_clicked']}",
                    f"Ventanas abiertas: {stats['windows_opened']}"
                ]
            }

        except Exception as e:
            logger.error(f"❌ Error en sesión: {e}")
            import traceback
            traceback.print_exc()
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
