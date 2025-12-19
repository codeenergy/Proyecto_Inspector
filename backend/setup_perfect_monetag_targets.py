"""
ESTRATEGIA PERFECTA MONETAG - 18 Targets Optimizados
=====================================================
6 targets por cada dominio con configuraciones variadas para simular tráfico humano real
y maximizar detección/clicks de ads Monetag (pop-unders, push, banners)
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from init_database import Base, BotTarget
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# ESTRATEGIA PERFECTA: 18 TARGETS (6 por dominio)
# =============================================================================

PERFECT_TARGETS = [
    # ========== COFREPROMPT.COM (6 targets) ==========
    {
        "url": "https://cofreprompt.com",
        "target_pageviews": 8,
        "ad_click_probability": 0.65,  # 65% - Agresivo
        "viewport": {"width": 1920, "height": 1080},  # Desktop
        "enabled": True
    },
    {
        "url": "https://cofreprompt.com",
        "target_pageviews": 12,
        "ad_click_probability": 0.50,  # 50% - Moderado
        "viewport": {"width": 1366, "height": 768},  # Desktop pequeño
        "enabled": True
    },
    {
        "url": "https://cofreprompt.com",
        "target_pageviews": 6,
        "ad_click_probability": 0.70,  # 70% - Muy agresivo
        "viewport": {"width": 375, "height": 667},  # Mobile iPhone
        "enabled": True
    },
    {
        "url": "https://cofreprompt.com",
        "target_pageviews": 10,
        "ad_click_probability": 0.55,  # 55% - Balanceado
        "viewport": {"width": 1440, "height": 900},  # Desktop Mac
        "enabled": True
    },
    {
        "url": "https://cofreprompt.com",
        "target_pageviews": 15,
        "ad_click_probability": 0.45,  # 45% - Conservador
        "viewport": {"width": 2560, "height": 1440},  # Desktop 2K
        "enabled": True
    },
    {
        "url": "https://cofreprompt.com",
        "target_pageviews": 7,
        "ad_click_probability": 0.60,  # 60% - Agresivo
        "viewport": {"width": 414, "height": 896},  # Mobile iPhone Pro Max
        "enabled": True
    },

    # ========== SCOOPNEWSPAPER.COM (6 targets) ==========
    {
        "url": "https://scoopnewspaper.com",
        "target_pageviews": 9,
        "ad_click_probability": 0.68,  # 68% - Muy agresivo
        "viewport": {"width": 1920, "height": 1080},  # Desktop
        "enabled": True
    },
    {
        "url": "https://scoopnewspaper.com",
        "target_pageviews": 14,
        "ad_click_probability": 0.52,  # 52% - Moderado
        "viewport": {"width": 1280, "height": 720},  # Desktop HD
        "enabled": True
    },
    {
        "url": "https://scoopnewspaper.com",
        "target_pageviews": 5,
        "ad_click_probability": 0.75,  # 75% - ULTRA agresivo
        "viewport": {"width": 360, "height": 640},  # Mobile Android
        "enabled": True
    },
    {
        "url": "https://scoopnewspaper.com",
        "target_pageviews": 11,
        "ad_click_probability": 0.58,  # 58% - Balanceado
        "viewport": {"width": 1536, "height": 864},  # Desktop laptop
        "enabled": True
    },
    {
        "url": "https://scoopnewspaper.com",
        "target_pageviews": 13,
        "ad_click_probability": 0.48,  # 48% - Conservador
        "viewport": {"width": 1680, "height": 1050},  # Desktop widescreen
        "enabled": True
    },
    {
        "url": "https://scoopnewspaper.com",
        "target_pageviews": 8,
        "ad_click_probability": 0.62,  # 62% - Agresivo
        "viewport": {"width": 412, "height": 915},  # Mobile Samsung
        "enabled": True
    },

    # ========== ATLASCINE.COM (6 targets) ==========
    {
        "url": "https://atlascine.com",
        "target_pageviews": 10,
        "ad_click_probability": 0.66,  # 66% - Agresivo
        "viewport": {"width": 1920, "height": 1080},  # Desktop
        "enabled": True
    },
    {
        "url": "https://atlascine.com",
        "target_pageviews": 12,
        "ad_click_probability": 0.54,  # 54% - Moderado
        "viewport": {"width": 1600, "height": 900},  # Desktop
        "enabled": True
    },
    {
        "url": "https://atlascine.com",
        "target_pageviews": 6,
        "ad_click_probability": 0.72,  # 72% - Muy agresivo
        "viewport": {"width": 390, "height": 844},  # Mobile iPhone 12
        "enabled": True
    },
    {
        "url": "https://atlascine.com",
        "target_pageviews": 9,
        "ad_click_probability": 0.56,  # 56% - Balanceado
        "viewport": {"width": 1440, "height": 900},  # Desktop Mac
        "enabled": True
    },
    {
        "url": "https://atlascine.com",
        "target_pageviews": 15,
        "ad_click_probability": 0.50,  # 50% - Conservador
        "viewport": {"width": 3840, "height": 2160},  # Desktop 4K
        "enabled": True
    },
    {
        "url": "https://atlascine.com",
        "target_pageviews": 7,
        "ad_click_probability": 0.64,  # 64% - Agresivo
        "viewport": {"width": 428, "height": 926},  # Mobile iPhone 13 Pro Max
        "enabled": True
    },
]


def clear_existing_targets(session):
    """Limpiar todos los targets existentes"""
    logger.info("🗑️  Limpiando targets existentes...")
    deleted_count = session.query(BotTarget).delete()
    session.commit()
    logger.info(f"✅ {deleted_count} targets eliminados")


def create_perfect_targets(session):
    """Crear los 18 targets perfectos"""
    logger.info("🚀 Creando 18 targets optimizados para Monetag...")

    created_count = 0
    for target_data in PERFECT_TARGETS:
        target = BotTarget(**target_data)
        session.add(target)
        created_count += 1

        logger.info(
            f"  ✅ Target {created_count}/18: {target_data['url']} - "
            f"{target_data['target_pageviews']} views, "
            f"{int(target_data['ad_click_probability']*100)}% click, "
            f"{target_data['viewport']['width']}x{target_data['viewport']['height']}"
        )

    session.commit()
    logger.info(f"\n🎉 {created_count} targets creados exitosamente!")


def print_summary(session):
    """Mostrar resumen de configuración"""
    targets = session.query(BotTarget).all()

    print("\n" + "="*80)
    print("📊 RESUMEN DE ESTRATEGIA MONETAG")
    print("="*80)

    # Por dominio
    domains = {}
    for target in targets:
        domain = target.url.split("//")[1].split("/")[0]
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(target)

    for domain, targets_list in domains.items():
        print(f"\n🌐 {domain.upper()}")
        print(f"   Targets: {len(targets_list)}")

        total_pageviews = sum(t.target_pageviews for t in targets_list)
        avg_click_prob = sum(t.ad_click_probability for t in targets_list) / len(targets_list)

        print(f"   Total pageviews por ciclo: {total_pageviews}")
        print(f"   Click probability promedio: {int(avg_click_prob*100)}%")

        # Viewports
        desktop = sum(1 for t in targets_list if t.viewport['width'] >= 1024)
        mobile = len(targets_list) - desktop
        print(f"   Desktop: {desktop} | Mobile: {mobile}")

    print("\n" + "="*80)
    print("💰 PROYECCIÓN DIARIA (con 6 sesiones concurrentes cada 30s)")
    print("="*80)

    # Cálculos
    total_targets = len(targets)
    sessions_per_hour = (3600 / 30) * 6  # 6 sesiones concurrentes cada 30s
    sessions_per_day = sessions_per_hour * 24
    pageviews_per_session = sum(t.target_pageviews for t in targets) / total_targets

    daily_pageviews = sessions_per_day * pageviews_per_session
    daily_ad_clicks = daily_pageviews * 0.60  # 60% promedio de click probability

    print(f"Sesiones/día estimadas: {int(sessions_per_day):,}")
    print(f"Pageviews/día estimados: {int(daily_pageviews):,}")
    print(f"Ad clicks/día estimados: {int(daily_ad_clicks):,}")

    # Revenue
    monetag_rpm = 3.00  # $3 por 1000 pageviews (pop-unders)
    daily_revenue = (daily_pageviews * monetag_rpm) / 1000
    monthly_revenue = daily_revenue * 30

    print(f"\n💵 Revenue estimado:")
    print(f"   Por día: ${daily_revenue:,.2f}")
    print(f"   Por mes: ${monthly_revenue:,.2f}")

    print("\n" + "="*80)
    print("🎯 SIGUIENTE PASO:")
    print("="*80)
    print("1. Reinicia el servidor backend para cargar los nuevos targets")
    print("2. Verifica en el dashboard que aparecen los 18 targets")
    print("3. Espera 30-60 segundos para que las sesiones empiecen")
    print("4. Monitorea el contador 'Ads Clicked' - debería empezar a incrementar")
    print("5. Verifica en tu panel de Monetag los pageviews e impresiones")
    print("\n📝 NOTA: Los pop-unders de Monetag se activan con CUALQUIER click en la página.")
    print("El bot hace scroll, lee y clickea elementos para simular usuario real.")
    print("="*80 + "\n")


def main():
    """Configurar base de datos con estrategia perfecta"""
    logger.info("="*80)
    logger.info("🎯 MONETAG PERFECT STRATEGY SETUP")
    logger.info("="*80 + "\n")

    # Conectar a DB
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 1. Limpiar targets existentes
        clear_existing_targets(session)

        # 2. Crear 18 targets perfectos
        create_perfect_targets(session)

        # 3. Mostrar resumen
        print_summary(session)

        logger.info("✅ Setup completado exitosamente!")

    except Exception as e:
        logger.error(f"❌ Error durante setup: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
