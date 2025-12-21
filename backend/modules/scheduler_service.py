"""
Servicio de Scheduler 24/7 con APScheduler
Ejecuta verificaciones periódicas de campañas
"""
import asyncio
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import logging

from config import settings

# Optional imports - gracefully handle if dependencies are missing
try:
    from modules.user_simulator import UserSimulator
    USER_SIMULATOR_AVAILABLE = True
except ImportError as e:
    logging.warning(f"User simulator not available (Playwright missing?): {e}")
    UserSimulator = None
    USER_SIMULATOR_AVAILABLE = False

try:
    from modules.alert_system import AlertSystem
except ImportError as e:
    logging.warning(f"Alert system not available: {e}")
    AlertSystem = None

try:
    from modules.ai_analyzer import analyze_error_with_ai
except ImportError as e:
    logging.warning(f"AI analyzer not available: {e}")
    analyze_error_with_ai = None

logger = logging.getLogger(__name__)


class BotTrafficScheduler:
    """
    Scheduler para tráfico automatizado con auto-recovery
    """

    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone='UTC')
        self.running_sessions: Dict[str, bool] = {}
        self.failed_sessions: Dict[str, int] = {}  # Track retry counts
        self.max_retries = 3
        self.max_concurrent_sessions = 2  # MODO LENTO: 2 sesiones max (parece humano)
        self.active_session_count = 0  # Track active sessions globally
        self.stats = {
            "total_sessions": 0,
            "total_pageviews": 0,
            "total_ad_clicks": 0,
            "total_failures": 0
        }

        # Add event listeners for error monitoring
        self.scheduler.add_listener(
            self._job_error_listener,
            EVENT_JOB_ERROR
        )
        self.scheduler.add_listener(
            self._job_executed_listener,
            EVENT_JOB_EXECUTED
        )

    def load_targets(self):
        """Cargar targets activos de la DB"""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        # Robust import fix
        import sys
        if str(Path(__file__).parent.parent) not in sys.path:
             sys.path.append(str(Path(__file__).parent.parent))

        from init_database import BotTarget # Importar modelo localmente para evitar ciclos
        
        try:
            engine = create_engine(settings.DATABASE_URL)
            Session = sessionmaker(bind=engine)
            session = Session()
            
            targets = session.query(BotTarget).filter_by(enabled=True).all()
            
            results = []
            for t in targets:
                results.append({
                    "id": t.id,
                    "url": t.url,
                    "target_pageviews": t.target_pageviews,
                    "ad_click_probability": t.ad_click_probability,
                    "viewport": t.viewport
                })
                
            session.close()
            return results
        except Exception as e:
            logger.error(f"Error cargando targets: {e}")
            return []

    def _job_error_listener(self, event):
        """Listener para errores en jobs - auto-recovery"""
        logger.error(f"❌ Job error: {event.exception}")
        logger.error(f"Job ID: {event.job_id}")
        # Stats tracking
        self.stats["total_failures"] = self.stats.get("total_failures", 0) + 1

    def _job_executed_listener(self, event):
        """Listener para jobs ejecutados exitosamente"""
        logger.debug(f"✅ Job executed successfully: {event.job_id}")

    def start(self):
        """Iniciar scheduler con auto-restart capability"""
        logger.info("🚀 Iniciando Bot de Tráfico 24/7...")

        try:
            # MODO LENTO: Revisar targets cada 5-10 minutos (parece tráfico humano)
            import random
            interval_seconds = random.randint(300, 600)  # 5-10 minutos aleatorio
            self.scheduler.add_job(
                self._check_and_launch_sessions,
                IntervalTrigger(seconds=interval_seconds),
                id="master_controller",
                name="Controlador de Sesiones (MODO LENTO)",
                replace_existing=True,  # Replace if already exists
                misfire_grace_time=120  # Allow 2min grace time
            )

            self.scheduler.start()
            logger.info("✅ Scheduler activo y operando 24/7. Esperando ciclo de control...")
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
            # Try to recover
            if not self.scheduler.running:
                logger.info("Attempting to restart scheduler...")
                self.scheduler.start()

    async def _check_and_launch_sessions(self):
        """Verificar targets y lanzar nuevas sesiones si es necesario"""
        targets = self.load_targets()
        logger.info(f"Targets activos encontrados: {len(targets)}")

        # LIMIT: Check global concurrent session limit (Railway memory constraint)
        if self.active_session_count >= self.max_concurrent_sessions:
            logger.debug(f"⏸️ Max concurrent sessions ({self.max_concurrent_sessions}) reached, waiting...")
            return

        for target in targets:
            target_id = str(target["id"])

            # Si ya hay una sesión corriendo para este target, saltar
            if self.running_sessions.get(target_id, False):
                logger.debug(f"Sesión ya activa para target {target_id}, saltando.")
                continue

            # Check global limit again before launching
            if self.active_session_count >= self.max_concurrent_sessions:
                logger.debug(f"⏸️ Concurrent limit reached, deferring remaining targets")
                break

            # Lanzar nueva sesión en background
            self.scheduler.add_job(
                self._run_session_job,
                trigger=None, # Run once immediately (fire and forget managed by scheduler exectuor)
                args=[target],
                id=f"session_{target_id}_{int(datetime.now().timestamp())}",
                name=f"Sesión {target['url']}",
                max_instances=1  # LIMIT: Only 1 instance per target
            )

            self.active_session_count += 1  # Increment counter

    async def _run_session_job(self, target_config: Dict):
        """Ejecutar una sesión de tráfico con retry logic y error recovery"""
        target_id = str(target_config["id"])
        self.running_sessions[target_id] = True

        start_time = datetime.utcnow()
        retry_count = self.failed_sessions.get(target_id, 0)

        # Ensure we have active session slot
        if self.active_session_count <= 0:
            self.active_session_count = 1  # Safety check

        try:
            logger.info(f"▶️ Iniciando sesión para {target_config['url']} (intento {retry_count + 1}/{self.max_retries})")

            # Check if user simulator is available
            if not USER_SIMULATOR_AVAILABLE:
                logger.error("❌ User simulator not available - Playwright may not be installed")
                result = {
                    "success": False,
                    "stats": {"pages_visited": 0, "ads_clicked": 0},
                    "log": ["User simulator unavailable - Playwright not installed"]
                }
            else:
                from modules.user_simulator import run_bot_session
                result = await run_bot_session(target_config)

            # Si la sesión fue exitosa, reset retry counter
            if result.get("success"):
                self.failed_sessions[target_id] = 0

                # Actualizar stats en memoria
                self.stats["total_sessions"] += 1
                pages_visited = 0
                ads_clicked = 0
                if result.get("stats"):
                    pages_visited = result["stats"].get("pages_visited", 0)
                    ads_clicked = result["stats"].get("ads_clicked", 0)
                    self.stats["total_pageviews"] += pages_visited
                    self.stats["total_ad_clicks"] += ads_clicked

                logger.info(f"✅ Sesión finalizada exitosamente: {result['stats']}")
            else:
                # Session failed, increment retry counter
                self.failed_sessions[target_id] = retry_count + 1
                self.stats["total_failures"] = self.stats.get("total_failures", 0) + 1
                logger.warning(f"⚠️ Sesión falló para target {target_id}")

            # --- PERSISTENCIA EN BBDD con retry ---
            for db_attempt in range(3):  # Try 3 times to save to DB
                try:
                    from sqlalchemy import create_engine
                    from sqlalchemy.orm import sessionmaker

                    # Robust import
                    import sys
                    if str(Path(__file__).parent.parent) not in sys.path:
                        sys.path.append(str(Path(__file__).parent.parent))

                    from init_database import BotSession

                    engine = create_engine(settings.DATABASE_URL)
                    Session = sessionmaker(bind=engine)
                    session = Session()

                    # Calcular duración
                    end_time = datetime.utcnow()
                    duration = (end_time - start_time).total_seconds()

                    pages_visited = 0
                    ads_clicked = 0
                    if result.get("stats"):
                        pages_visited = result["stats"].get("pages_visited", 0)
                        ads_clicked = result["stats"].get("ads_clicked", 0)

                    new_session = BotSession(
                        target_id=target_config["id"],
                        start_time=start_time,
                        end_time=end_time,
                        duration_seconds=duration,
                        pages_visited=pages_visited,
                        ads_clicked=ads_clicked,
                        status="completed" if result.get("success") else "failed",
                        log=json.dumps(result.get("log", [])[:10])
                    )

                    session.add(new_session)
                    session.commit()
                    session.close()
                    logger.debug("✅ Sesión guardada en DB")
                    break  # Success, exit retry loop

                except Exception as db_e:
                    logger.error(f"Error guardando sesión en DB (intento {db_attempt + 1}/3): {db_e}")
                    if db_attempt < 2:  # Not last attempt
                        await asyncio.sleep(2 ** db_attempt)  # Exponential backoff: 1s, 2s
                    else:
                        logger.error("❌ Failed to save session to DB after 3 attempts")
            # ---------------------------

        except Exception as e:
            logger.error(f"❌ Error crítico en sesión {target_id}: {e}")
            self.failed_sessions[target_id] = retry_count + 1
            self.stats["total_failures"] = self.stats.get("total_failures", 0) + 1

            # Auto-retry if under max retries
            if self.failed_sessions[target_id] < self.max_retries:
                wait_time = 2 ** self.failed_sessions[target_id]  # Exponential backoff
                logger.info(f"🔄 Reintentando sesión {target_id} en {wait_time}s...")
                await asyncio.sleep(wait_time)
                # Re-queue the job
                self.scheduler.add_job(
                    self._run_session_job,
                    trigger=None,
                    args=[target_config],
                    id=f"retry_session_{target_id}_{int(datetime.now().timestamp())}",
                    name=f"Retry {target_config['url']}"
                )
            else:
                logger.error(f"❌ Max retries reached for target {target_id}. Will try again in next cycle.")
                self.failed_sessions[target_id] = 0  # Reset for next cycle

        finally:
            self.running_sessions[target_id] = False
            # Decrement active session counter to allow next session
            if self.active_session_count > 0:
                self.active_session_count -= 1
            logger.debug(f"Active sessions: {self.active_session_count}/{self.max_concurrent_sessions}")

    def stop(self):
        self.scheduler.shutdown(wait=False)

    def get_status(self):
        return {
            "running": self.scheduler.running,
            "active_sessions": sum(1 for v in self.running_sessions.values() if v),
            "stats": self.stats
        }

# Singleton global
_scheduler_instance: Optional[BotTrafficScheduler] = None

def get_scheduler() -> BotTrafficScheduler:
    """Obtener instancia singleton del scheduler"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = BotTrafficScheduler()
    return _scheduler_instance
