"""
Script de inicialización de base de datos
Crea tablas y estructura inicial
"""
import asyncio
import logging
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


# Modelos de base de datos
class BotTarget(Base):
    __tablename__ = "bot_targets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False)
    enabled = Column(Boolean, default=True)
    
    # Configuración de comportamiento
    target_pageviews = Column(Integer, default=10)  # Páginas a visitar por sesión
    min_duration_seconds = Column(Integer, default=60)  # Tiempo mínimo en el sitio
    ad_click_probability = Column(Float, default=0.2)  # Probabilidad de click en anuncio (0.0 a 1.0)
    
    # Configuración técnica
    viewport = Column(JSON, default={"width": 1920, "height": 1080})
    user_agent = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BotSession(Base):
    __tablename__ = "bot_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    target_id = Column(Integer, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    duration_seconds = Column(Float)
    pages_visited = Column(Integer, default=0)
    ads_clicked = Column(Integer, default=0)
    buttons_clicked = Column(Integer, default=0)  # NUEVO: Botones clickeados
    windows_opened = Column(Integer, default=0)   # NUEVO: Ventanas/Direct Links abiertas
    status = Column(String(50), default="running")  # running, completed, failed
    log = Column(Text)  # Log resumen de la sesión

    
def init_database():
    """Inicializar base de datos"""
    logger.info("Inicializando base de datos...")
    logger.info(f"Database URL: {settings.DATABASE_URL}")

    # Crear engine
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DB_ECHO
    )

    # Crear todas las tablas (solo si no existen)
    # IMPORTANTE: No usar drop_all en producción para preservar datos
    if settings.ENVIRONMENT == "development":
        logger.warning("🔄 Modo desarrollo: Reiniciando base de datos...")
        Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)

    logger.info("✅ Base de datos inicializada correctamente")

    # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()

    # Verificar si ya existe un target (no crear duplicados)
    existing_targets = session.query(BotTarget).count()

    if existing_targets == 0:
        # Crear target por defecto solo si no hay ninguno
        default_target = BotTarget(
            url="https://example.com",
            target_pageviews=5,
            ad_click_probability=0.3,
            viewport={"width": 1366, "height": 768}
        )
        session.add(default_target)
        session.commit()
        logger.info("✅ Target por defecto creado")
    else:
        logger.info(f"ℹ️ Base de datos ya tiene {existing_targets} targets")

    session.close()
    engine.dispose()

    return True

def seed_sample_data():
    pass # No needed anymore


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Inicializar base de datos")
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Insertar datos de ejemplo"
    )

    args = parser.parse_args()

    try:
        init_database()

        if args.seed:
            seed_sample_data()

        logger.info("🎉 Inicialización completada exitosamente")

    except Exception as e:
        logger.exception(f"❌ Error en inicialización: {e}")
        exit(1)
