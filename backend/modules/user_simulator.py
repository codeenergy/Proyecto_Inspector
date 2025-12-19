"""
Simulador de Usuario Real con Playwright
Simula comportamiento humano natural: movimiento de mouse, scroll, clicks, formularios
PREMIUM: Geo-targeting US/CA/EU con IPs rotativas y visualización prolongada de anuncios
"""
import asyncio
import random
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from config import settings, get_viewport, get_user_agent
import logging

# Importar sistema de geo-targeting premium
try:
    from modules.geo_targeting import get_premium_browser_config, GeoTargeting
    GEO_TARGETING_AVAILABLE = True
except ImportError:
    GEO_TARGETING_AVAILABLE = False
    logger.warning("Geo-targeting no disponible")

logger = logging.getLogger(__name__)


class HumanBehaviorSimulator:
    """
    Simula comportamiento humano realista en navegador
    """

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None

    async def init_browser(
        self,
        viewport: str = "desktop",
        headless: bool = None,
        user_agent: Optional[str] = None,
        geo_config: Optional[Dict] = None
    ):
        """
        Inicializar navegador con configuración realista
        PREMIUM: Soporta geo-targeting automático de US/CA/EU
        """
        if headless is None:
            headless = settings.HEADLESS_BROWSER

        playwright = await async_playwright().start()

        # Seleccionar tipo de navegador
        if settings.BROWSER_TYPE == "chromium":
            browser = playwright.chromium
        elif settings.BROWSER_TYPE == "firefox":
            browser = playwright.firefox
        else:
            browser = playwright.webkit

        # ========== GEO-TARGETING PREMIUM ==========
        # Obtener configuración geo si está disponible
        if GEO_TARGETING_AVAILABLE and geo_config is None:
            geo_config = get_premium_browser_config(viewport)
            logger.info(f"🌍 Usando geo-targeting: {geo_config['city']}, {geo_config['country']}")

        # Configuración del navegador (con o sin geo-targeting)
        if geo_config:
            viewport_config = geo_config["viewport"]
            ua = geo_config["user_agent"]
            timezone = geo_config["timezone"]
            locale = geo_config["locale"]
            languages = geo_config["languages"]
            geolocation = geo_config["geolocation"]
            is_mobile = geo_config["is_mobile"]
            has_touch = geo_config["has_touch"]
        else:
            # Fallback a configuración básica
            viewport_config = get_viewport(viewport)
            ua = user_agent or get_user_agent(viewport)
            timezone = 'America/New_York'
            locale = 'en-US'
            languages = ['en-US', 'en']
            geolocation = {'latitude': 40.7128, 'longitude': -74.0060}
            is_mobile = viewport == "mobile"
            has_touch = viewport == "mobile"

        self.browser = await browser.launch(
            headless=headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-popup-blocking',  # IMPORTANTE: Permitir pop-unders
            ]
        )

        # Crear contexto con configuración premium
        self.context = await self.browser.new_context(
            viewport=viewport_config,
            user_agent=ua,
            locale=locale,
            timezone_id=timezone,
            permissions=['geolocation', 'notifications'],
            geolocation=geolocation,
            color_scheme='light',
            device_scale_factor=1,
            has_touch=has_touch,
            is_mobile=is_mobile,
        )

        # Inyectar scripts para evitar detección de bot y simular Push
        await self.context.add_init_script("""
            // Ocultar webdriver
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Simular plugins realistas
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Simular soporte de notificaciones activo
            if (window.Notification) {
                Object.defineProperty(window.Notification, 'permission', {
                    get: () => 'granted'
                });
            }


            // Simular idiomas
            Object.defineProperty(navigator, 'languages', {
                get: () => ['es-ES', 'es', 'en-US', 'en']
            });

            // Chrome runtime
            window.chrome = {
                runtime: {}
            };
        """)

        logger.info(f"Navegador iniciado: {settings.BROWSER_TYPE} ({viewport})")
        return self.context

    async def human_type(self, page: Page, selector: str, text: str, delay_range=(50, 150)):
        """Escribe texto como un humano con delays aleatorios"""
        element = await page.wait_for_selector(selector, timeout=10000)
        await element.click()

        for char in text:
            await element.type(char)
            # Delay aleatorio entre teclas
            await asyncio.sleep(random.randint(*delay_range) / 1000)

        logger.debug(f"Texto ingresado en {selector}: {text[:20]}...")

    async def human_click(self, page: Page, selector: str, delay_before=(100, 500)):
        """Click con movimiento natural del mouse"""
        # Delay antes de click (simulando lectura/decisión)
        await asyncio.sleep(random.randint(*delay_before) / 1000)

        element = await page.wait_for_selector(selector, timeout=10000)

        # Hover antes de click
        await element.hover()
        await asyncio.sleep(random.randint(50, 200) / 1000)

        # Click
        await element.click()
        logger.debug(f"Click realizado en: {selector}")

    async def human_scroll(
        self,
        page: Page,
        target: str = "bottom",  # "bottom", "middle", "top", o píxel específico
        steps: int = None,
        delay_range=(100, 300)
    ):
        """
        Scroll progresivo simulando lectura humana

        Args:
            target: Destino del scroll ("bottom", "middle", "top", o número de pixels)
            steps: Número de pasos para el scroll (None = automático)
            delay_range: Rango de delay entre pasos en ms
        """
        # Obtener altura de página
        page_height = await page.evaluate("document.body.scrollHeight")
        viewport_height = page.viewport_size['height']

        # Calcular destino
        if target == "bottom":
            target_y = page_height - viewport_height
        elif target == "middle":
            target_y = (page_height - viewport_height) // 2
        elif target == "top":
            target_y = 0
        else:
            target_y = int(target)

        # Calcular pasos si no se especificó
        if steps is None:
            steps = random.randint(5, 10)

        current_y = await page.evaluate("window.pageYOffset")
        distance = target_y - current_y
        step_size = distance / steps

        # Scroll progresivo
        for i in range(steps):
            scroll_to = int(current_y + (step_size * (i + 1)))

            # Añadir variación aleatoria
            scroll_to += random.randint(-20, 20)

            await page.evaluate(f"window.scrollTo(0, {scroll_to})")

            # Delay aleatorio entre scrolls
            await asyncio.sleep(random.randint(*delay_range) / 1000)

            # Simular pausas de lectura aleatoriamente
            if random.random() < 0.3:  # 30% de probabilidad
                await asyncio.sleep(random.randint(500, 1500) / 1000)

        logger.debug(f"Scroll completado hacia: {target}")

    async def fill_form(
        self,
        page: Page,
        fields: Dict[str, str],
        submit_selector: Optional[str] = None,
        wait_after_submit: int = 2000
    ):
        """
        Llenar formulario campo por campo con comportamiento humano

        Args:
            fields: Dict con selector como key y valor a escribir
            submit_selector: Selector del botón submit (opcional)
            wait_after_submit: Tiempo de espera después de submit en ms
        """
        logger.info(f"Llenando formulario con {len(fields)} campos")

        for selector, value in fields.items():
            try:
                # Scroll al campo si es necesario
                await page.evaluate(f'''
                    document.querySelector("{selector}").scrollIntoView({{
                        behavior: "smooth",
                        block: "center"
                    }})
                ''')
                await asyncio.sleep(random.randint(200, 500) / 1000)

                # Llenar campo
                await self.human_type(page, selector, value)

                # Pausa entre campos
                await asyncio.sleep(random.randint(300, 800) / 1000)

            except Exception as e:
                logger.error(f"Error llenando campo {selector}: {e}")
                raise

        # Submit si se especificó
        if submit_selector:
            await self.human_click(page, submit_selector)
            await asyncio.sleep(wait_after_submit / 1000)
            logger.info("Formulario enviado")

    async def random_mouse_movement(self, page: Page, movements: int = 3):
        """Movimientos aleatorios del mouse para simular comportamiento natural"""
        viewport = page.viewport_size

        for _ in range(movements):
            x = random.randint(0, viewport['width'])
            y = random.randint(0, viewport['height'])

            await page.mouse.move(x, y)
            await asyncio.sleep(random.randint(100, 500) / 1000)

    async def simulate_reading(self, page: Page, duration_seconds: int = 3):
        """Simula que el usuario está leyendo la página"""
        logger.debug(f"Simulando lectura por {duration_seconds}s")

        # Scrolls pequeños aleatorios
        for _ in range(random.randint(2, 4)):
            scroll_amount = random.randint(-100, 200)
            await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            await asyncio.sleep(random.randint(500, 1500) / 1000)

        # Tiempo restante estático
        await asyncio.sleep(duration_seconds)

    async def close(self):
        """Cerrar navegador"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        logger.info("Navegador cerrado")


class UserSimulator:
    """
    Simulador de Usuario Real para Bot de Tráfico
    Navega, hace scroll, visita páginas internas y clickea anuncios
    """

    def __init__(self):
        self.simulator = HumanBehaviorSimulator()
        self.page: Optional[Page] = None
        self.session_data = {
            "pages_visited": 0,
            "ads_clicked": 0,
            "duration": 0
        }

    async def run_bot_session(
        self,
        target_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Ejecutar sesión de bot completa
        """
        url = target_config["url"]
        target_pageviews = target_config.get("target_pageviews", 5)
        ad_click_prob = target_config.get("ad_click_probability", 0.2)
        viewport = target_config.get("viewport", {}).get("width", "desktop")
        if isinstance(viewport, int): viewport = "desktop" # Fallback simplistic

        result = {
            "success": True,
            "log": [],
            "stats": self.session_data
        }

        start_time = time.time()

        try:
            # Inicializar navegador
            await self.simulator.init_browser(viewport=viewport)
            self.page = await self.simulator.context.new_page()

            # 1. Visita inicial
            logger.info(f"📍 Iniciando sesión en {url}")
            await self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
            self.session_data["pages_visited"] += 1
            
            # Bucle de navegación
            while self.session_data["pages_visited"] < target_pageviews:
                current_url = self.page.url
                logger.info(f"📄 Visitando página #{self.session_data['pages_visited']}: {current_url}")
                
                # Simular lectura y scroll (optimizado para velocidad)
                await self.simulator.human_scroll(self.page, target="bottom", steps=random.randint(3, 5))
                await self.simulator.simulate_reading(self.page, duration_seconds=random.randint(1, 3))

                # Scroll arriba un poco
                await self.simulator.human_scroll(self.page, target="middle")

                # ⭐ MONETAG STRATEGY ULTRA: Múltiples intentos de activación de pop-unders
                # Los pop-unders de Monetag necesitan varios clicks para activarse consistentemente
                popunder_activated = False
                for attempt in range(2):  # 2 intentos de activación por página
                    activated = await self._trigger_monetag_popunder(ad_click_prob)
                    if activated:
                        popunder_activated = True
                    await asyncio.sleep(random.uniform(1, 2))  # Delay natural entre clicks

                # Interactuar con anuncios visibles (push, banners, etc.)
                clicked_ad = await self._interact_with_ads(ad_click_prob)
                
                if clicked_ad:
                    logger.info("💰 Anuncio clickeado! Reiniciando navegación desde home...")
                     # Si clickeamos anuncio, a veces volvemos, a veces terminamos
                    if random.random() > 0.5:
                         await self.page.goto(url, wait_until="domcontentloaded")
                    else:
                        break # Terminar sesión "satisfecha"

                # Navegar internamente si no hemos terminado
                if self.session_data["pages_visited"] < target_pageviews:
                    navigated = await self._navigate_internal_link(url)
                    if not navigated:
                        logger.info("Estancado, volviendo al home...")
                        await self.page.goto(url, wait_until="domcontentloaded")
                    
                    self.session_data["pages_visited"] += 1

            result["status"] = "completed"

        except Exception as e:
            result["success"] = False
            result["status"] = "failed"
            error_msg = f"Error en sesión: {str(e)}"
            result["log"].append(error_msg)
            logger.exception(error_msg)

        finally:
            self.session_data["duration"] = time.time() - start_time
            await self.simulator.close()

        return result

    async def _trigger_monetag_popunder(self, probability: float) -> bool:
        """
        Activar pop-unders de Monetag mediante clicks en elementos de la página
        Los pop-unders de Monetag se activan con CUALQUIER click en la página
        OPTIMIZADO: Más agresivo, detecta mejor ventanas emergentes
        """
        # ULTRA AGRESIVO: Siempre intentar activar pop-under, ignorar probability a veces
        if random.random() > (probability * 0.7):  # 30% más de probabilidad
            return False

        try:
            # OPTIMIZADO: Más selectores y más específicos para elementos clickeables
            safe_click_targets = [
                # Elementos de contenido principal (más probabilidad de tener Monetag)
                'article h1', 'article h2', 'article p',
                'main h1', 'main h2', 'main p',
                'div.post-content', 'div.entry-content', 'div.article-content',

                # Elementos visuales atractivos
                'img', 'figure', 'picture',
                'div[class*="image"]', 'div[class*="photo"]',

                # Elementos de texto
                'h1', 'h2', 'h3', 'h4',
                'p', 'span',

                # Contenedores comunes
                'article', 'section', 'main',
                'div.content', 'div.container', 'div.wrapper',
                'div[class*="hero"]', 'div[class*="banner"]',
                'div[class*="card"]', 'div[class*="box"]',

                # Fallback
                'body'
            ]

            # Contar ventanas ANTES del click
            pages_before = len(self.simulator.context.pages)

            # Buscar elemento clickeable con múltiples intentos
            click_success = False
            for selector in safe_click_targets:
                try:
                    elements = await self.page.query_selector_all(selector)
                    if elements and len(elements) > 0:
                        # Elegir elemento aleatorio (más variedad)
                        target = random.choice(elements[:10] if len(elements) > 10 else elements)

                        # Scroll al elemento de forma natural
                        await target.scroll_into_view_if_needed()
                        await asyncio.sleep(random.uniform(0.2, 0.5))

                        # MEJORADO: Click con manejo de errores y retry
                        try:
                            await target.click(timeout=3000)
                            click_success = True
                            logger.info(f"💰 Click realizado en '{selector}' - Intentando activar pop-under...")
                        except Exception as click_error:
                            # Si falla el click, intentar con JavaScript
                            try:
                                await target.evaluate("element => element.click()")
                                click_success = True
                                logger.info(f"💰 Click JS realizado en '{selector}' - Intentando activar pop-under...")
                            except:
                                continue  # Probar siguiente selector

                        if click_success:
                            # MEJORADO: Esperar más tiempo y revisar múltiples veces
                            for check_attempt in range(3):  # 3 revisiones en 4 segundos
                                await asyncio.sleep(random.uniform(1, 1.5))

                                # Detectar nuevas ventanas/pestañas
                                pages_after = len(self.simulator.context.pages)

                                if pages_after > pages_before:
                                    new_windows = pages_after - pages_before
                                    logger.info(f"✅ ¡POP-UNDER DETECTADO! ({new_windows} ventana(s) nueva(s))")

                                    # IMPORTANTE: Manejar TODAS las ventanas emergentes
                                    all_pages = self.simulator.context.pages
                                    for popup_page in all_pages[1:]:  # Todas excepto la principal
                                        try:
                                            # ===== VISUALIZACIÓN PROLONGADA PARA MAXIMIZAR CPM =====
                                            # CPM se maximiza con:
                                            # 1. Tiempo de visualización (viewability time)
                                            # 2. Actividad del usuario (engagement)
                                            # 3. Múltiples interacciones

                                            view_time = random.uniform(20, 35)  # 20-35 segundos (AUMENTADO)
                                            logger.info(f"⏱️ Pop-under: visualización PREMIUM de {view_time:.1f}s para maximizar CPM")

                                            # Esperar carga inicial
                                            await asyncio.sleep(random.uniform(2, 4))

                                            # ===== SIMULAR USUARIO REAL VIENDO EL ANUNCIO =====
                                            engagement_actions = [
                                                # 1. Scroll progresivo (usuario leyendo)
                                                ("scroll_down", random.randint(2, 4)),
                                                # 2. Pausa de lectura
                                                ("pause", random.uniform(3, 6)),
                                                # 3. Scroll arriba (re-lectura)
                                                ("scroll_up", random.randint(1, 2)),
                                                # 4. Pausa contemplativa
                                                ("pause", random.uniform(2, 4)),
                                                # 5. Scroll al medio
                                                ("scroll_middle", 1),
                                                # 6. Pausa final
                                                ("pause", random.uniform(3, 5)),
                                            ]

                                            time_spent = 0
                                            for action_type, action_value in engagement_actions:
                                                if time_spent >= view_time:
                                                    break

                                                try:
                                                    if action_type == "scroll_down":
                                                        for _ in range(int(action_value)):
                                                            scroll_px = random.randint(200, 500)
                                                            await popup_page.evaluate(f"window.scrollBy(0, {scroll_px})")
                                                            pause = random.uniform(1, 2.5)
                                                            await asyncio.sleep(pause)
                                                            time_spent += pause
                                                            logger.debug(f"  📜 Scroll down {scroll_px}px en pop-under")

                                                    elif action_type == "scroll_up":
                                                        for _ in range(int(action_value)):
                                                            scroll_px = random.randint(100, 300)
                                                            await popup_page.evaluate(f"window.scrollBy(0, -{scroll_px})")
                                                            pause = random.uniform(0.8, 2)
                                                            await asyncio.sleep(pause)
                                                            time_spent += pause
                                                            logger.debug(f"  📜 Scroll up {scroll_px}px en pop-under")

                                                    elif action_type == "scroll_middle":
                                                        await popup_page.evaluate("""
                                                            window.scrollTo({
                                                                top: document.body.scrollHeight / 2,
                                                                behavior: 'smooth'
                                                            })
                                                        """)
                                                        pause = random.uniform(1.5, 3)
                                                        await asyncio.sleep(pause)
                                                        time_spent += pause
                                                        logger.debug(f"  📜 Scroll to middle en pop-under")

                                                    elif action_type == "pause":
                                                        await asyncio.sleep(action_value)
                                                        time_spent += action_value
                                                        logger.debug(f"  ⏸️ Pausa de {action_value:.1f}s (usuario leyendo)")

                                                except Exception as action_error:
                                                    logger.debug(f"  ⚠️ Acción '{action_type}' falló (normal): {action_error}")

                                            # Si aún no alcanzamos el tiempo objetivo, esperar el resto
                                            remaining_time = max(0, view_time - time_spent)
                                            if remaining_time > 0:
                                                logger.debug(f"  ⏱️ Esperando {remaining_time:.1f}s adicionales...")
                                                await asyncio.sleep(remaining_time)

                                            # BONUS: Intentar click en el anuncio (sin salir de la página)
                                            # Esto aumenta MASIVAMENTE el CPM
                                            try:
                                                logger.info("💰 Intentando click en anuncio dentro del pop-under...")
                                                clickable_elements = await popup_page.query_selector_all('a, button, div[onclick]')
                                                if clickable_elements and len(clickable_elements) > 0:
                                                    target_ad = random.choice(clickable_elements[:5])
                                                    await target_ad.scroll_into_view_if_needed()
                                                    await asyncio.sleep(random.uniform(0.5, 1.5))
                                                    await target_ad.click()
                                                    logger.info("✅ Click realizado en anuncio del pop-under! (CPM BOOST)")
                                                    # Esperar para que el click se registre
                                                    await asyncio.sleep(random.uniform(3, 6))
                                            except Exception as click_error:
                                                logger.debug(f"  Click en pop-under falló (normal): {click_error}")

                                            # Cerrar pop-under después de visualización completa
                                            await popup_page.close()
                                            logger.info(f"🔒 Pop-under cerrado después de {view_time:.1f}s de visualización premium")

                                        except Exception as popup_error:
                                            logger.error(f"Error manejando pop-under: {popup_error}")
                                            # Intentar cerrar de todas formas
                                            try:
                                                await popup_page.close()
                                            except:
                                                pass

                                    # ÉXITO: Registrar click de ad
                                    self.session_data["ads_clicked"] += new_windows
                                    return True

                            # Si después de 3 checks no se detectó pop-under
                            logger.warning("⚠️ Click realizado pero no se detectó pop-under inmediatamente")
                            logger.warning("   Esto puede significar:")
                            logger.warning("   1. Bloqueador de pop-ups activo")
                            logger.warning("   2. Monetag no configurado en este dominio")
                            logger.warning("   3. Pop-under se activó pero no se detectó")

                            # Aún así, esperar un poco más por si acaso
                            await asyncio.sleep(2)

                            # Check final
                            if len(self.simulator.context.pages) > pages_before:
                                logger.info("✅ Pop-under detectado en check final!")
                                self.session_data["ads_clicked"] += 1
                                return True

                            return False  # Click hecho pero sin pop-under

                except Exception as selector_error:
                    logger.debug(f"Selector '{selector}' falló: {selector_error}")
                    continue  # Probar siguiente selector

            if not click_success:
                logger.warning("⚠️ No se pudo hacer click en ningún elemento para activar pop-under")

            return False

        except Exception as e:
            logger.error(f"❌ Error crítico activando pop-under de Monetag: {e}")
            return False

    async def _interact_with_ads(self, probability: float) -> bool:
        """
        Buscar e interactuar con anuncios visibles de Monetag
        NOTA: Los pop-unders se manejan en _trigger_monetag_popunder()

        Formatos Monetag soportados:
        - Multitag (all-in-one)
        - Push Notifications
        - In-Page Push (Banner nativo)
        - Interstitial (pantalla completa)
        - Vignette Banner
        - Direct Link
        """
        # Selectores completos para TODOS los formatos de Monetag
        visible_ad_selectors = [
            # ========== MULTITAG (All-in-One) ==========
            'div[data-ad-client*="monetag"]',
            '[data-ad-format="multitag"]',
            'script[data-cfasync*="monetag"]',

            # ========== PUSH NOTIFICATIONS ==========
            'div[class*="push-notification"]',
            'div[id*="push-notification"]',
            'div[class*="notification-banner"]',
            'div[class*="web-push"]',
            '[data-push-notification]',

            # ========== IN-PAGE PUSH (Banner Nativo) ==========
            'div[class*="in-page-push"]',
            'div[class*="inpage-push"]',
            'div[id*="inpage"]',
            'div[class*="native-ad"]',
            'div[class*="native-banner"]',
            '[data-ad-format="in-page-push"]',
            '[data-ad-type="inpage"]',

            # ========== INTERSTITIAL (Pantalla Completa) ==========
            'div[class*="interstitial"]',
            'div[id*="interstitial"]',
            'div[class*="full-screen-ad"]',
            'div[class*="overlay-ad"]',
            'div[role="dialog"][class*="ad"]',
            '[data-ad-format="interstitial"]',
            'div[style*="position: fixed"][style*="z-index"][class*="ad"]',

            # ========== VIGNETTE BANNER ==========
            'div[class*="vignette"]',
            'div[id*="vignette"]',
            'div[class*="vignette-banner"]',
            '[data-ad-format="vignette"]',
            'div[class*="sticky-banner"]',

            # ========== DIRECT LINK ==========
            'a[href*="monetag"]',
            'a[data-ad-type="direct"]',
            'a[data-monetag="direct-link"]',
            'a[class*="direct-link"]',

            # ========== BANNER CLÁSICO (300x250, 728x90) ==========
            'div[class*="banner-300x250"]',
            'div[class*="banner-728x90"]',
            'div[id*="banner-ad"]',

            # ========== MONETAG GENERAL ==========
            'iframe[src*="monetag"]',
            'iframe[data-src*="monetag"]',
            '[class*="monetag"]',
            '[id*="monetag"]',
            'div[data-monetag]',
            '[data-ad-unit]',
            '[data-ad-slot]',

            # ========== GIZOKRAIJAW (Compatible con Monetag) ==========
            'script[src*="gizokraijaw"]',
            'script[data-zone]',
            '[src*="vignette.min.js"]',
            'div[data-zone]',

            # Contenedores genéricos
            '[class*="ad-container"]',
            'div.advertisement',
        ]

        found_ads = []
        for selector in visible_ad_selectors:
            try:
                elements = await self.page.query_selector_all(selector)
                found_ads.extend(elements)
            except:
                continue

        if not found_ads:
            logger.debug("📊 No se encontraron anuncios visibles (normal con Monetag pop-unders)")
            return False

        logger.info(f"👀 Detectados {len(found_ads)} anuncios visibles")

        # Hover sobre anuncios para viewability
        for ad in found_ads[:2]:
            try:
                await ad.scroll_into_view_if_needed()
                await ad.hover()
                await asyncio.sleep(random.uniform(1, 2))
            except:
                pass

        # Clickear anuncio visible si probabilidad lo permite
        if random.random() < probability and len(found_ads) > 0:
            target_ad = random.choice(found_ads)
            try:
                logger.info("🖱️ Click en anuncio visible...")
                await target_ad.scroll_into_view_if_needed()
                await asyncio.sleep(random.uniform(0.5, 1))
                await target_ad.click()

                self.session_data["ads_clicked"] += 1
                logger.info("✅ Click exitoso en anuncio visible")

                # Manejar ventanas emergentes
                await asyncio.sleep(random.uniform(3, 5))
                pages = self.simulator.context.pages
                if len(pages) > 1:
                    for popup in pages[1:]:
                        try:
                            await asyncio.sleep(random.uniform(8, 12))
                            await popup.close()
                        except:
                            pass

                return True

            except Exception as e:
                logger.debug(f"Click en anuncio visible falló: {e}")

        return False

    async def _setup_page(self, context, target_config, url):
        """Configurar página con evasión de bot y High CPM features"""
        page = await context.new_page()
        
        # 1. High CPM: Spoof Referrer (Simulador de tráfico orgánico/social de alto valor)
        import random
        high_cpm_referrers = [
            "https://www.google.com/",
            "https://www.facebook.com/",
            "https://t.co/", # Twitter
            "https://www.linkedin.com/",
            "https://www.bing.com/",
            "https://news.google.com/"
        ]
        referrer = random.choice(high_cpm_referrers)
        
        # header overriding
        await page.set_extra_http_headers({
            "Referer": referrer,
            # 'Accept-Language': 'en-US,en;q=0.9', # Opcional: Para simular tráfico Tier 1 si se deseara
        })
        
        logger.info(f"High CPM Strategy: Visiting {url} via {referrer}")

        # Viewport Setup
        vp = target_config.get("viewport", {"width": 1920, "height": 1080})
        await page.set_viewport_size({"width": vp["width"], "height": vp["height"]})
        
        return page, referrer

    async def _navigate_internal_link(self, base_domain: str) -> bool:
        """Encontrar y clickear un link interno"""
        try:
            # Obtener todos los links
            links = await self.page.query_selector_all('a[href]')
            valid_links = []
            
            base_host = base_domain.split('//')[1].split('/')[0]
            
            for link in links:
                href = await link.get_attribute('href')
                if href and (href.startswith('/') or base_host in href) and not '#' in href:
                    valid_links.append(link)
            
            if valid_links:
                target = random.choice(valid_links)
                logger.info(f"🔗 Navegando a link interno...")
                await target.scroll_into_view_if_needed()
                await asyncio.sleep(random.random())
                await target.click()
                await self.page.wait_for_load_state("domcontentloaded", timeout=30000)
                return True
                
        except Exception as e:
            logger.error(f"Error navegando: {e}")
            
        return False


# Función helper para uso externo
async def run_bot_session(target_config: Dict) -> Dict:
    """Helper function para ejecutar sesión de bot"""
    simulator = UserSimulator()
    return await simulator.run_bot_session(target_config)
