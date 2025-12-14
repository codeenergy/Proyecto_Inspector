"""
Simulador de Usuario Real con Playwright
Simula comportamiento humano natural: movimiento de mouse, scroll, clicks, formularios
"""
import asyncio
import random
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from config import settings, get_viewport, get_user_agent
import logging

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
        user_agent: Optional[str] = None
    ):
        """Inicializar navegador con configuración realista"""
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

        # Configuración del navegador
        viewport_config = get_viewport(viewport)
        ua = user_agent or get_user_agent(viewport)

        self.browser = await browser.launch(
            headless=headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )

        # Crear contexto con configuración realista
        self.context = await self.browser.new_context(
            viewport=viewport_config,
            user_agent=ua,
            locale='es-ES',
            timezone_id='America/New_York',
            permissions=['geolocation', 'notifications'],
            geolocation={'latitude': 40.7128, 'longitude': -74.0060},  # NYC
            color_scheme='light',
            device_scale_factor=1,
            has_touch=viewport == "mobile",
            is_mobile=viewport == "mobile",
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
                
                # Simular lectura y scroll
                await self.simulator.human_scroll(self.page, target="bottom", steps=random.randint(5, 12))
                await self.simulator.simulate_reading(self.page, duration_seconds=random.randint(5, 15))
                
                # Scroll arriba un poco
                await self.simulator.human_scroll(self.page, target="middle")

                # Interactuar con anuncios
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

    async def _interact_with_ads(self, probability: float) -> bool:
        """Buscar e interactuar con anuncios - Optimizado para Monetag"""
        # Selectores específicos para Monetag y otros ad networks
        ad_selectors = [
            # Google Ads
            'iframe[src*="googleads"]',
            'iframe[id*="google_ads"]',
            '.adsbygoogle',
            'div[id*="div-gpt-ad"]',
            'a[href*="doubleclick"]',
            '[aria-label="Advertisement"]',

            # ========== MONETAG ESPECÍFICO ==========
            # Push Notifications (Monetag)
            'div[id*="push-notification"]',
            'div[class*="push-notification"]',
            '[id*="monetag-push"]',
            '[class*="monetag-push"]',
            'div[data-monetag-type="push"]',

            # Direct Link (Monetag) - Links que abren en nueva pestaña
            'a[target="_blank"][href*="monetag"]',
            'a[target="_blank"][href*="propellerads"]',
            'a[data-monetag="direct-link"]',

            # In-Page Push (Monetag) - Notificaciones dentro de la página
            'div[class*="in-page-push"]',
            'div[id*="in-page-push"]',
            '[class*="inpage-push"]',
            '[id*="inpage"]',
            'div[class*="native-ad"]',
            'div[data-ad-format="in-page-push"]',

            # Vignette Banner (Monetag) - Anuncios de página completa
            'div[class*="vignette"]',
            'div[id*="vignette"]',
            'div[class*="interstitial"]',
            'div[id*="interstitial"]',
            'div[style*="position: fixed"][style*="z-index"]',
            'div[data-ad-format="vignette"]',

            # Monetag General
            'iframe[src*="monetag"]',
            'iframe[data-src*="monetag"]',
            '[class*="monetag"]',
            '[id*="monetag"]',
            'script[src*="monetag"]',
            '[href*="monetag"]',
            'div[data-monetag]',

            # PropellerAds (similar a Monetag)
            '[class*="propeller"]',
            '[id*="propeller"]',
            'iframe[src*="propellerads"]',

            # Genéricos de alto CPM
            'div.ad-container',
            'div[class*="popup"]',
            'div[class*="overlay"]',
            'div[style*="z-index: 2147483647"]', # Max Z-Index
            'div[class*="pusher"]',
            'div[class*="notification-banner"]',
            'div[role="dialog"]', # Popups modales
            '[data-ad-unit]',
            '[data-ad-slot]'
        ]
        
        found_ads = []
        for selector in ad_selectors:
            elements = await self.page.query_selector_all(selector)
            found_ads.extend(elements)
            
        if not found_ads:
            return False

        logger.info(f"👀 Detectados {len(found_ads)} posibles espacios publicitarios")
        
        # Hover sobre algunos anuncios (viewability)
        for ad in found_ads[:3]:
            try:
                await ad.scroll_into_view_if_needed()
                await ad.hover()
                await asyncio.sleep(random.random() * 2)
            except: pass

        # Decidir si clickear (aumentado para Monetag)
        if random.random() < probability:
            target_ad = random.choice(found_ads)
            try:
                logger.info("🖱️ Intentando click en anuncio Monetag...")

                # Detectar tipo de anuncio Monetag
                ad_class = await target_ad.get_attribute('class') or ''
                ad_id = await target_ad.get_attribute('id') or ''
                ad_type = "unknown"

                if 'push' in ad_class.lower() or 'push' in ad_id.lower():
                    ad_type = "Push Notification"
                elif 'vignette' in ad_class.lower() or 'vignette' in ad_id.lower():
                    ad_type = "Vignette Banner"
                elif 'in-page' in ad_class.lower() or 'inpage' in ad_id.lower():
                    ad_type = "In-Page Push"
                elif 'direct' in ad_class.lower() or await target_ad.get_attribute('target') == '_blank':
                    ad_type = "Direct Link"

                logger.info(f"💰 Detectado anuncio tipo: {ad_type}")

                # Click en el anuncio (Ctrl+Click para abrir en nueva pestaña)
                await target_ad.scroll_into_view_if_needed()
                await asyncio.sleep(random.uniform(0.5, 1.5))
                await target_ad.click(modifiers=["Control"])

                # Registrar click exitoso
                self.session_data["ads_clicked"] += 1
                logger.info(f"✅ Click exitoso en anuncio {ad_type}")

                # Esperar a que se abra la nueva pestaña/popup (tiempo realista)
                await asyncio.sleep(random.uniform(5, 10))

                # Cerrar pestañas extra (Monetag a veces abre múltiples)
                pages = self.simulator.context.pages
                if len(pages) > 1:
                    logger.info(f"🔄 Cerrando {len(pages) - 1} pestañas de anuncios...")
                    for p in pages[1:]:
                        try:
                            # AUMENTADO: Permanece 15-30 segundos en cada anuncio como usuario real
                            # Esto MAXIMIZA el revenue (viewability + engagement)
                            wait_time = random.uniform(15, 30)
                            logger.info(f"⏱️ Permaneciendo {wait_time:.1f}s en anuncio (aumentando revenue)")
                            await asyncio.sleep(wait_time)

                            # Simular scroll en la página del anuncio (engagement realista)
                            try:
                                await p.evaluate("window.scrollBy(0, window.innerHeight / 2)")
                                await asyncio.sleep(random.uniform(2, 5))
                                await p.evaluate("window.scrollBy(0, -window.innerHeight / 4)")
                            except:
                                pass

                            await p.close()
                        except:
                            pass

                return True

            except Exception as e:
                logger.error(f"❌ Falló click en anuncio: {e}")
                # Intentar click simple si Ctrl+Click falló
                try:
                    await target_ad.click()
                    self.session_data["ads_clicked"] += 1
                    await asyncio.sleep(3)
                    return True
                except:
                    pass

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
