"""
Script de prueba para Undetected Chrome
Ejecutar: python test_undetected.py
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
        "target_pageviews": 3,
        "ad_click_probability": 0.8,
        "viewport": {"width": 1920, "height": 1080}
    }
    
    print("🚀 Iniciando prueba de Undetected Chrome...")
    print("=" * 60)
    
    result = await run_undetected_session(config)
    
    print("=" * 60)
    print("📊 RESULTADO:")
    print(f"  ✅ Success: {result['success']}")
    print(f"  📄 Páginas: {result['stats']['pages_visited']}")
    print(f"  💰 Ads: {result['stats']['ads_clicked']}")
    print(f"  🎯 Popups: {result['stats']['popups_detected']}")

if __name__ == "__main__":
    asyncio.run(test())
