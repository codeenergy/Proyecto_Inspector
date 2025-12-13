"""
Ad-Inspector Bot - Main Entry Point
Inicializa y coordina todos los servicios
"""
import asyncio
import logging
import sys
import signal
from pathlib import Path
import argparse
from datetime import datetime

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from modules.scheduler_service import get_scheduler
from api.server import app
import uvicorn

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOGS_DIR / f"inspector_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class AdInspectorBot:
    """
    Clase principal del bot
    Coordina scheduler, API y servicios
    """

    def __init__(self, headless: bool = True, api_enabled: bool = True):
        self.headless = headless
        self.api_enabled = api_enabled
        self.scheduler = get_scheduler()
        self.running = False

        # Signal handlers para shutdown graceful
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handler para señales de sistema (Ctrl+C, etc.)"""
        logger.info(f"Señal {signum} recibida, iniciando shutdown...")
        self.stop()
        sys.exit(0)

    def start(self):
        """Iniciar todos los servicios"""
        logger.info("=" * 80)
        logger.info(f"🤖 Ad-Inspector Bot v{settings.APP_VERSION}")
        logger.info(f"Ambiente: {settings.ENVIRONMENT}")
        logger.info(f"Headless: {self.headless}")
        logger.info("=" * 80)

        try:
            self.running = True

            # Iniciar API si está habilitada
            if self.api_enabled:
                logger.info(f"Iniciando API REST en {settings.API_HOST}:{settings.API_PORT}...")
                # El scheduler se iniciará en el lifespan de FastAPI (api/server.py)
                self._start_api()
            else:
                # Si no hay API, iniciar scheduler y mantener vivo
                logger.info("Modo headless - iniciando scheduler...")
                
                # Necesitamos un event loop para AsyncIOScheduler
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                self.scheduler.start()
                logger.info("✅ Scheduler activo (Headless)")
                
                try:
                    loop.run_forever()
                except (KeyboardInterrupt, SystemExit):
                    pass
                finally:
                    self.scheduler.stop()
                    loop.close()

            return True

        except Exception as e:
            logger.exception(f"Error crítico en inicio: {e}")
            return False

    def _start_api(self):
        """Iniciar servidor API"""
        try:
            uvicorn.run(
                app,
                host=settings.API_HOST,
                port=settings.API_PORT,
                log_level=settings.LOG_LEVEL.lower(),
                access_log=True
            )

        except Exception as e:
            logger.exception(f"Error iniciando API: {e}")
            raise

    def _keep_alive(self):
        """Mantener el proceso vivo en modo headless"""
        logger.info("Bot activo. Presiona Ctrl+C para detener...")

        try:
            while self.running:
                asyncio.get_event_loop().run_until_complete(asyncio.sleep(60))

                # Log heartbeat cada hora
                if datetime.now().minute == 0:
                    status = self.scheduler.get_status()
                    logger.info(
                        f"💓 Heartbeat - Checks: {status['stats']['total_checks']} - "
                        f"Jobs activos: {status['total_jobs']}"
                    )

        except KeyboardInterrupt:
            logger.info("Shutdown solicitado por usuario")
            self.stop()

    def stop(self):
        """Detener todos los servicios"""
        logger.info("Deteniendo Ad-Inspector Bot...")

        self.running = False

        # Detener scheduler
        if self.scheduler.scheduler.running:
            self.scheduler.stop()
            logger.info("✅ Scheduler detenido")

        logger.info("👋 Ad-Inspector Bot detenido correctamente")

    def get_status(self):
        """Obtener estado actual del bot"""
        return {
            "running": self.running,
            "scheduler": self.scheduler.get_status(),
            "config": {
                "environment": settings.ENVIRONMENT,
                "headless": self.headless,
                "api_enabled": self.api_enabled
            }
        }


def main():
    """Entry point principal"""
    parser = argparse.ArgumentParser(
        description="Ad-Inspector Bot - Monitoreo 24/7 de anuncios y conversiones"
    )

    parser.add_argument(
        "--headless",
        action="store_true",
        help="Ejecutar en modo headless (sin API, solo scheduler)"
    )

    parser.add_argument(
        "--no-api",
        action="store_true",
        help="Deshabilitar API REST"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path al archivo de configuración de campañas"
    )

    args = parser.parse_args()

    # Crear y arrancar bot
    bot = AdInspectorBot(
        headless=args.headless,
        api_enabled=not args.no_api
    )

    try:
        bot.start()
    except KeyboardInterrupt:
        logger.info("Shutdown por Ctrl+C")
        bot.stop()
    except Exception as e:
        logger.exception(f"Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
