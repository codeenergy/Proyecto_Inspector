"""
Verificador de URLs - Checks HTTP rápidos sin navegador
"""
import aiohttp
import time
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


async def check_url(
    url: str,
    timeout: int = 10,
    follow_redirects: bool = True
) -> Dict:
    """
    Verificación HTTP rápida de URL

    Returns:
        {
            "url": str,
            "status_code": int,
            "response_time_ms": float,
            "is_ok": bool,
            "error": Optional[str]
        }
    """
    result = {
        "url": url,
        "status_code": None,
        "response_time_ms": None,
        "is_ok": False,
        "error": None,
        "redirected_to": None
    }

    try:
        start_time = time.time()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=timeout),
                allow_redirects=follow_redirects
            ) as response:
                response_time = (time.time() - start_time) * 1000  # ms

                result["status_code"] = response.status
                result["response_time_ms"] = round(response_time, 2)
                result["is_ok"] = 200 <= response.status < 400

                if str(response.url) != url:
                    result["redirected_to"] = str(response.url)

                logger.debug(
                    f"URL Check: {url} -> {response.status} "
                    f"({response_time:.0f}ms)"
                )

    except aiohttp.ClientError as e:
        result["error"] = f"Client error: {str(e)}"
        logger.error(f"Error checking {url}: {e}")

    except asyncio.TimeoutError:
        result["error"] = f"Timeout after {timeout}s"
        logger.error(f"Timeout checking {url}")

    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
        logger.exception(f"Unexpected error checking {url}")

    return result


async def check_multiple_urls(urls: list, concurrency: int = 5) -> Dict[str, Dict]:
    """
    Verificar múltiples URLs concurrentemente

    Args:
        urls: Lista de URLs a verificar
        concurrency: Número máximo de requests concurrentes

    Returns:
        Dict con URL como key y resultado como value
    """
    semaphore = asyncio.Semaphore(concurrency)

    async def check_with_semaphore(url):
        async with semaphore:
            return await check_url(url)

    results = await asyncio.gather(
        *[check_with_semaphore(url) for url in urls],
        return_exceptions=True
    )

    return {
        urls[i]: (results[i] if not isinstance(results[i], Exception) else {"error": str(results[i])})
        for i in range(len(urls))
    }
