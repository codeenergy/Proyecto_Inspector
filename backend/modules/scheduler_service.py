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
from modules.user_simulator import UserSimulator
from modules.alert_system import AlertSystem
from modules.ai_analyzer import analyze_error_with_ai

logger = logging.getLogger(__name__)


class BotTrafficScheduler:
    """
    Scheduler para tráfico automatizado
    """

    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone='UTC')
        self.running_sessions: Dict[str, bool] = {}
        self.stats = {
            "total_sessions": 0,
            "total_pageviews": 0,
            "total_ad_clicks": 0
        }

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

    def start(self):
        """Iniciar scheduler"""
        logger.info("🚀 Iniciando Bot de Tráfico...")
        
        # Job maestro que revisa targets cada 30 segundos y lanza sesiones
        self.scheduler.add_job(
            self._check_and_launch_sessions,
            IntervalTrigger(seconds=30),
            id="master_controller",
            name="Controlador de Sesiones"
        )
        
        self.scheduler.start()
        logger.info("✅ Scheduler activo. Esperando ciclo de control...")

    async def _check_and_launch_sessions(self):
        """Verificar targets y lanzar nuevas sesiones si es necesario"""
        targets = self.load_targets()
        logger.info(f"Targets activos encontrados: {len(targets)}")
        
        for target in targets:
            target_id = str(target["id"])
            
            # Si ya hay una sesión corriendo para este target, saltar
            if self.running_sessions.get(target_id, False):
                logger.debug(f"Sesión ya activa para target {target_id}, saltando.")
                continue
                
            # Lanzar nueva sesión en background
            self.scheduler.add_job(
                self._run_session_job,
                trigger=None, # Run once immediately (fire and forget managed by scheduler exectuor)
                args=[target],
                id=f"session_{target_id}_{int(datetime.now().timestamp())}",
                name=f"Sesión {target['url']}",
                max_instances=5
            )

    async def _run_session_job(self, target_config: Dict):
        """Ejecutar una sesión de tráfico completa"""
        target_id = str(target_config["id"])
        self.running_sessions[target_id] = True
        
        start_time = datetime.utcnow() # Track start time manually for DB
        
        try:
            logger.info(f"▶️ Iniciando sesión para {target_config['url']}")
            
            from modules.user_simulator import run_bot_session
            result = await run_bot_session(target_config)
            
            # Actualizar stats en memoria
            self.stats["total_sessions"] += 1
            pages_visited = 0
            ads_clicked = 0
            if result.get("stats"):
                pages_visited = result["stats"].get("pages_visited", 0)
                ads_clicked = result["stats"].get("ads_clicked", 0)
                self.stats["total_pageviews"] += pages_visited
                self.stats["total_ad_clicks"] += ads_clicked
            
            logger.info(f"⏹️ Sesión finalizada: {result['stats']}")
            
            # --- PERSISTENCIA EN BBDD ---
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
                
                new_session = BotSession(
                    target_id=target_config["id"],
                    start_time=start_time,
                    end_time=end_time,
                    duration_seconds=duration,
                    pages_visited=pages_visited,
                    ads_clicked=ads_clicked,
                    status="completed" if result.get("success") else "failed",
                    log=json.dumps(result.get("log", [])[:10]) # Guardar resumen de log si existe
                )
                
                session.add(new_session)
                session.commit()
                session.close()
                logger.debug("✅ Sesión guardada en DB")
                
            except Exception as db_e:
                logger.error(f"Error guardando sesión en DB: {db_e}")
            # ---------------------------
            
        except Exception as e:
            logger.error(f"Error en sesión {target_id}: {e}")
        finally:
            self.running_sessions[target_id] = False

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
