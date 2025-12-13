"""
Web Explorer - Navegación Completa como Usuario Real
Explora dominios completos, hace click en TODO (botones, enlaces, anuncios)
"""
import asyncio
import random
import time
import re
from typing import Dict, List, Set, Optional
from urllib.parse import urljoin, urlparse
from playwright.async_api import Page, Browser
import logging

from modules.user_simulator import HumanBehaviorSimulator
from config import settings

logger = logging.getLogger(__name__)


class WebExplorer:
    """
    Explora un dominio completo como usuario real
    - Hace click en todos los botones
    - Sigue todos los enlaces
    - Detecta y hace click en anuncios
    - Llena formularios
    - Mapea toda la estructura del sitio
    """

    def __init__(self, base_url: str, max_depth: int = 3, max_pages: int = 50):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.max_depth = max_depth
        self.max_pages = max_pages

        self.visited_urls: Set[str] = set()
        self.found_buttons: List[Dict] = []
        self.found_links: List[Dict] = []
        self.found_ads: List[Dict] = []
        self.found_forms: List[Dict] = []

        self.simulator = HumanBehaviorSimulator()
        self.page: Optional[Page] = None

    async def explore_domain(self, viewport: str = "desktop") -> Dict:
        """
        Exploración completa de un dominio

        Returns:
            {
                "base_url": str,
                "total_pages_visited": int,
                "total_buttons_clicked": int,
                "total_links_followed": int,
                "total_ads_found": int,
                "total_forms_found": int,
                "sitemap": List[Dict],
                "screenshots": List[str]
            }
        """
        logger.info(f"🚀 Iniciando exploración de {self.base_url}")

        result = {
            "base_url": self.base_url,
            "total_pages_visited": 0,
            "total_buttons_clicked": 0,
            "total_links_followed": 0,
            "total_ads_found": 0,
            "total_forms_found": 0,
            "sitemap": [],
            "screenshots": []
        }

        try:
            # Inicializar navegador
            await self.simulator.init_browser(viewport=viewport)
            self.page = await self.simulator.context.new_page()

            # Explorar desde la URL base
            await self._explore_page(self.base_url, depth=0)

            # Compilar resultados
            result["total_pages_visited"] = len(self.visited_urls)
            result["total_buttons_clicked"] = len(self.found_buttons)
            result["total_links_followed"] = len([l for l in self.found_links if l.get("clicked")])
            result["total_ads_found"] = len(self.found_ads)
            result["total_forms_found"] = len(self.found_forms)
            result["sitemap"] = list(self.visited_urls)

            logger.info(
                f"✅ Exploración completada: "
                f"{result['total_pages_visited']} páginas, "
                f"{result['total_buttons_clicked']} botones, "
                f"{result['total_ads_found']} anuncios"
            )

        except Exception as e:
            logger.exception(f"Error en exploración: {e}")

        finally:
            await self.simulator.close()

        return result

    async def _explore_page(self, url: str, depth: int):
        """Explorar una página específica"""

        # Límites de exploración
        if depth > self.max_depth:
            logger.debug(f"Profundidad máxima alcanzada en {url}")
            return

        if len(self.visited_urls) >= self.max_pages:
            logger.debug(f"Máximo de páginas alcanzado")
            return

        if url in self.visited_urls:
            logger.debug(f"URL ya visitada: {url}")
            return

        # Solo explorar mismo dominio
        if urlparse(url).netloc != self.base_domain:
            logger.debug(f"URL externa, saltando: {url}")
            return

        logger.info(f"📄 Explorando [{depth}]: {url}")
        self.visited_urls.add(url)

        try:
            # Navegar a la página
            await self.page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(random.uniform(1, 2))

            # Screenshot
            screenshot_path = settings.SCREENSHOTS_DIR / f"explore_{int(time.time())}_{depth}.png"
            await self.page.screenshot(path=str(screenshot_path))

            # Simular scroll de lectura
            await self.simulator.human_scroll(self.page, target="middle")
            await asyncio.sleep(random.uniform(0.5, 1.5))
            await self.simulator.human_scroll(self.page, target="bottom")

            # 1. DETECTAR Y HACER CLICK EN ANUNCIOS
            await self._detect_and_click_ads()

            # 2. DETECTAR Y HACER CLICK EN BOTONES
            await self._detect_and_click_buttons()

            # 3. DETECTAR FORMULARIOS
            await self._detect_forms()

            # 4. EXTRAER Y SEGUIR ENLACES
            links = await self._extract_links()

            # Seguir algunos enlaces (para no explotar la exploración)
            links_to_follow = random.sample(links, min(5, len(links)))

            for link in links_to_follow:
                link_url = link["url"]
                logger.debug(f"Siguiendo enlace: {link_url}")

                # Recursión para explorar enlace
                await self._explore_page(link_url, depth + 1)

                # Volver a la página anterior
                await self.page.goto(url, wait_until="networkidle")
                await asyncio.sleep(random.uniform(0.5, 1))

        except Exception as e:
            logger.error(f"Error explorando {url}: {e}")

    async def _detect_and_click_ads(self):
        """Detectar y hacer click en anuncios"""
        logger.debug("🎯 Detectando anuncios...")

        # Selectores comunes de anuncios
        ad_selectors = [
            # Google Ads
            'iframe[id*="google_ads"]',
            'iframe[src*="doubleclick"]',
            'iframe[src*="googlesyndication"]',
            'ins.adsbygoogle',
            '[data-ad-slot]',

            # Facebook Ads
            'iframe[src*="facebook.com/plugins"]',
            '[data-testid*="ad"]',

            # Genéricos
            '.ad', '.ads', '.advertisement', '.banner-ad',
            '[class*="ad-"]', '[id*="ad-"]',
            '[class*="banner"]', '[id*="banner"]',
            'a[href*="ad."]', 'a[href*="ads."]',

            # Affiliate links
            'a[href*="amazon-adsystem"]',
            'a[href*="awin1.com"]',
            'a[href*="clickbank"]',
        ]

        for selector in ad_selectors:
            try:
                elements = await self.page.query_selector_all(selector)

                for element in elements:
                    try:
                        # Verificar si es visible
                        is_visible = await element.is_visible()
                        if not is_visible:
                            continue

                        # Obtener información del anuncio
                        text = await element.text_content() or ""
                        href = await element.get_attribute("href") or ""

                        ad_info = {
                            "type": "ad",
                            "selector": selector,
                            "text": text[:100],
                            "href": href,
                            "page": self.page.url
                        }

                        self.found_ads.append(ad_info)
                        logger.info(f"📢 Anuncio encontrado: {selector} - {text[:50]}")

                        # Scroll al elemento
                        await element.scroll_into_view_if_needed()
                        await asyncio.sleep(random.uniform(0.3, 0.8))

                        # Hover
                        await element.hover()
                        await asyncio.sleep(random.uniform(0.2, 0.5))

                        # Click (puede abrir nueva pestaña)
                        try:
                            # Guardar página actual
                            current_pages = len(self.simulator.context.pages)

                            await element.click(timeout=5000)
                            await asyncio.sleep(random.uniform(1, 2))

                            # Si abrió nueva pestaña, cerrarla
                            new_pages = len(self.simulator.context.pages)
                            if new_pages > current_pages:
                                new_page = self.simulator.context.pages[-1]
                                logger.debug(f"Nueva pestaña abierta: {new_page.url}")
                                await new_page.close()

                        except Exception as e:
                            logger.debug(f"No se pudo hacer click en anuncio: {e}")

                    except Exception as e:
                        logger.debug(f"Error procesando elemento de anuncio: {e}")

            except Exception as e:
                logger.debug(f"Error con selector {selector}: {e}")

    async def _detect_and_click_buttons(self):
        """Detectar y hacer click en todos los botones"""
        logger.debug("🔘 Detectando botones...")

        # Selectores de botones
        button_selectors = [
            'button',
            'input[type="button"]',
            'input[type="submit"]',
            'a.btn', 'a.button',
            '[role="button"]',
            '.cta-button', '.call-to-action',
            '[class*="btn-"]',
        ]

        for selector in button_selectors:
            try:
                buttons = await self.page.query_selector_all(selector)

                for button in buttons:
                    try:
                        # Verificar si es visible
                        is_visible = await button.is_visible()
                        if not is_visible:
                            continue

                        # Obtener información
                        text = await button.text_content() or ""
                        text = text.strip()

                        # Ignorar botones de navegación que ya seguimos
                        skip_words = ['next', 'previous', 'back', 'close', 'cancel']
                        if any(word in text.lower() for word in skip_words):
                            continue

                        button_info = {
                            "type": "button",
                            "selector": selector,
                            "text": text,
                            "page": self.page.url
                        }

                        self.found_buttons.append(button_info)
                        logger.info(f"🔘 Botón encontrado: {text}")

                        # Scroll al botón
                        await button.scroll_into_view_if_needed()
                        await asyncio.sleep(random.uniform(0.2, 0.5))

                        # Hover
                        await button.hover()
                        await asyncio.sleep(random.uniform(0.2, 0.5))

                        # Click
                        try:
                            await button.click(timeout=5000)
                            await asyncio.sleep(random.uniform(1, 2))

                            # Verificar si se abrió modal o cambió algo
                            # Si se abrió modal, cerrar
                            close_selectors = [
                                '.modal .close', '.modal-close',
                                '[aria-label="Close"]',
                                'button:has-text("Close")',
                                'button:has-text("×")'
                            ]

                            for close_sel in close_selectors:
                                try:
                                    close_btn = await self.page.query_selector(close_sel)
                                    if close_btn and await close_btn.is_visible():
                                        await close_btn.click()
                                        await asyncio.sleep(0.5)
                                        break
                                except:
                                    pass

                        except Exception as e:
                            logger.debug(f"No se pudo hacer click en botón '{text}': {e}")

                    except Exception as e:
                        logger.debug(f"Error procesando botón: {e}")

            except Exception as e:
                logger.debug(f"Error con selector de botones {selector}: {e}")

    async def _detect_forms(self):
        """Detectar formularios en la página"""
        logger.debug("📝 Detectando formularios...")

        try:
            forms = await self.page.query_selector_all('form')

            for form in forms:
                try:
                    # Obtener campos del formulario
                    inputs = await form.query_selector_all('input, textarea, select')

                    fields = []
                    for input_elem in inputs:
                        input_type = await input_elem.get_attribute('type') or 'text'
                        input_name = await input_elem.get_attribute('name') or ''
                        input_id = await input_elem.get_attribute('id') or ''

                        fields.append({
                            "type": input_type,
                            "name": input_name,
                            "id": input_id
                        })

                    form_info = {
                        "page": self.page.url,
                        "fields": fields,
                        "num_fields": len(fields)
                    }

                    self.found_forms.append(form_info)
                    logger.info(f"📝 Formulario encontrado con {len(fields)} campos")

                except Exception as e:
                    logger.debug(f"Error procesando formulario: {e}")

        except Exception as e:
            logger.debug(f"Error detectando formularios: {e}")

    async def _extract_links(self) -> List[Dict]:
        """Extraer todos los enlaces de la página"""
        logger.debug("🔗 Extrayendo enlaces...")

        links = []

        try:
            link_elements = await self.page.query_selector_all('a[href]')

            for link in link_elements:
                try:
                    href = await link.get_attribute('href')
                    text = await link.text_content() or ""

                    # Resolver URL completa
                    full_url = urljoin(self.page.url, href)

                    # Solo enlaces del mismo dominio
                    if urlparse(full_url).netloc == self.base_domain:
                        link_info = {
                            "url": full_url,
                            "text": text.strip(),
                            "clicked": False
                        }

                        links.append(link_info)
                        self.found_links.append(link_info)

                except Exception as e:
                    logger.debug(f"Error extrayendo enlace: {e}")

        except Exception as e:
            logger.debug(f"Error extrayendo enlaces: {e}")

        logger.debug(f"🔗 {len(links)} enlaces internos encontrados")
        return links


# Función helper para uso externo
async def explore_website(url: str, max_depth: int = 2, max_pages: int = 30) -> Dict:
    """
    Explorar un sitio web completo

    Args:
        url: URL base del sitio
        max_depth: Profundidad máxima de exploración
        max_pages: Número máximo de páginas a visitar

    Returns:
        Diccionario con resultados de la exploración
    """
    explorer = WebExplorer(url, max_depth=max_depth, max_pages=max_pages)
    return await explorer.explore_domain()
