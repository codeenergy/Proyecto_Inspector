"""
Script de prueba simple para Undetected Chrome
"""
import asyncio
import sys
from pathlib import Path

# Añadir backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from modules.user_simulator_undetected import run_undetected_session

async def test():
    config = {
        "url": "https://cofreprompt.com",
        "target_pageviews": 2,
        "viewport": {"width": 1920, "height": 1080}
    }

    print("=" * 60)
    print("INICIANDO PRUEBA - MODO USUARIO NORMAL")
    print("Objetivo: Clickear TODOS los botones como usuario real")
    print("=" * 60)

    result = await run_undetected_session(config)

    print("\n" + "=" * 60)
    print("RESULTADO:")
    print("=" * 60)
    print(f"Success: {result['success']}")
    print(f"Paginas visitadas: {result['stats']['pages_visited']}")
    print(f"Botones clickeados: {result['stats']['buttons_clicked']}")
    print(f"Ventanas abiertas: {result['stats']['windows_opened']}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test())
