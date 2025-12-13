"""
API REST con FastAPI
Expone endpoints para el frontend y control del bot
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional
from pydantic import BaseModel
import logging
import sys
from pathlib import Path

# Add project root to sys.path to ensure imports work correctly
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from config import settings
from modules.scheduler_service import get_scheduler
from modules.ai_analyzer import analyze_campaign_error, generate_dashboard_insight
from modules.web_explorer import explore_website
from init_database import BotTarget, BotSession, init_database

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, Session

# Database setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing scheduler via lifespan...")
    scheduler = get_scheduler()
    if not scheduler.scheduler.running:
         scheduler.start()
    
    yield
    
    # Shutdown
    if scheduler.scheduler.running:
        scheduler.stop()

# Crear app FastAPI
app = FastAPI(
    title="Ad-Inspector Bot API",
    version="2024.07.1",
    description="API para control y monitoreo del Ad-Inspector Bot",
    lifespan=lifespan
)

# CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Models
class BotTargetCreate(BaseModel):
    url: str
    target_pageviews: int = 10
    ad_click_probability: float = 0.2
    viewport: Dict = {"width": 1920, "height": 1080}
    enabled: bool = True

class StatusResponse(BaseModel):
    status: str
    message: str


# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    scheduler = get_scheduler()
    return {
        "status": "healthy",
        "service": "traffic-bot-pro",
        "version": "2024.07.1",
        "scheduler_running": scheduler.scheduler.running
    }


# Scheduler Control
@app.post("/scheduler/start", response_model=StatusResponse)
async def start_scheduler():
    """Iniciar scheduler"""
    try:
        scheduler = get_scheduler()

        if scheduler.scheduler.running:
            return {
                "status": "warning",
                "message": "Scheduler ya está ejecutándose"
            }

        scheduler.start()

        return {
            "status": "success",
            "message": "Scheduler iniciado correctamente"
        }

    except Exception as e:
        logger.exception("Error iniciando scheduler")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scheduler/stop", response_model=StatusResponse)
async def stop_scheduler():
    """Detener scheduler"""
    try:
        scheduler = get_scheduler()

        if not scheduler.scheduler.running:
            return {
                "status": "warning",
                "message": "Scheduler no está corriendo"
            }

        scheduler.stop()

        return {
            "status": "success",
            "message": "Scheduler detenido correctamente"
        }

    except Exception as e:
        logger.exception("Error deteniendo scheduler")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scheduler/status")
async def get_scheduler_status():
    """Estado del scheduler"""
    scheduler = get_scheduler()
    return {
        "status": "success",
        "data": scheduler.get_status()
    }


# -- NEW BOT TARGET API --

@app.get("/targets")
async def get_targets(db: Session = Depends(get_db)):
    """Listar targets"""
    try:
        targets = db.query(BotTarget).all()
        return {
            "status": "success",
            "data": targets
        }
    except Exception as e:
        logger.exception("Error obteniendo targets")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/targets", response_model=StatusResponse)
async def create_target(target: BotTargetCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Crear nuevo target"""
    try:
        new_target = BotTarget(
            url=target.url,
            target_pageviews=target.target_pageviews,
            ad_click_probability=target.ad_click_probability,
            viewport=target.viewport,
            enabled=target.enabled
        )
        db.add(new_target)
        db.commit()
        db.refresh(new_target)
        
        # Reload scheduler in background to prevent blocking/errors affecting response
        background_tasks.add_task(reload_scheduler_safely)

        return {
            "status": "success",
            "message": "Target creado correctamente"
        }
    except Exception as e:
        logger.exception("Error creando target")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/targets/{target_id}", response_model=StatusResponse)
async def delete_target(target_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Eliminar target"""
    try:
        target = db.query(BotTarget).filter(BotTarget.id == target_id).first()
        if not target:
            raise HTTPException(status_code=404, detail="Target no encontrado")
            
        db.delete(target)
        db.commit()
        
        # Reload scheduler in background
        background_tasks.add_task(reload_scheduler_safely)

        return {
            "status": "success",
            "message": "Target eliminado correctamente"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error eliminando target {target_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")

@app.put("/targets/{target_id}", response_model=StatusResponse)
async def update_target(target_id: int, target_data: BotTargetCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Actualizar target"""
    try:
        target = db.query(BotTarget).filter(BotTarget.id == target_id).first()
        if not target:
            raise HTTPException(status_code=404, detail="Target no encontrado")
            
        target.url = target_data.url
        target.target_pageviews = target_data.target_pageviews
        target.ad_click_probability = target_data.ad_click_probability
        target.viewport = target_data.viewport
        target.enabled = target_data.enabled
        
        db.commit()
        
        # Reload scheduler in background
        background_tasks.add_task(reload_scheduler_safely)

        return {
            "status": "success",
            "message": "Target actualizado correctamente"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error actualizando target {target_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")

def reload_scheduler_safely():
    """Helper to reload scheduler without crashing API"""
    try:
        scheduler = get_scheduler()
        if scheduler:
            scheduler.load_targets()
    except Exception as e:
        logger.error(f"Error reloading scheduler in background: {e}")

@app.get("/sessions/live")
async def get_live_sessions(db: Session = Depends(get_db)):
    """Obtener logs de sesiones recientes (simulado 'en vivo')"""
    try:
        # Get last 20 sessions ordered by start_time
        recent_sessions = db.query(BotSession).order_by(desc(BotSession.start_time)).limit(20).all()
        
        logs = []
        for s in recent_sessions:
             logs.append({
                "id": s.id,
                "target_id": s.target_id,
                "status": s.status,
                "pages": s.pages_visited,
                "ads": s.ads_clicked,
                "duration": s.duration_seconds if s.duration_seconds else 0,
                "time": s.start_time.strftime("%H:%M:%S")
            })
        
        return {
            "status": "success",
            "data": logs
        }

    except Exception as e:
        logger.exception("Error obteniendo live logs")
        raise HTTPException(status_code=500, detail=str(e))


# Logs & Stats
@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Global stats endpoint (Persistent from DB)"""
    try:
        from sqlalchemy import func
        from init_database import BotSession
        
        # Aggregate stats using SQL for speed and persistence
        total_sessions = db.query(func.count(BotSession.id)).scalar() or 0
        total_pageviews = db.query(func.sum(BotSession.pages_visited)).scalar() or 0
        total_ad_clicks = db.query(func.sum(BotSession.ads_clicked)).scalar() or 0
        
        return {
            "status": "success",
            "data": {
                "stats": {
                    "total_sessions": total_sessions,
                    "total_pageviews": total_pageviews,
                    "total_ad_clicks": total_ad_clicks
                }
            }
        }
    except Exception as e:
        logger.error(f"Error calculating stats: {e}")
        # Fallback to empty if DB fails
        return {
            "status": "error",
            "data": {
                "stats": {
                    "total_sessions": 0,
                    "total_pageviews": 0,
                    "total_ad_clicks": 0
                }
            }
        }


# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc) if settings.DEBUG else None
        }
    )


if __name__ == "__main__":
    import uvicorn
    import os

    # Railway assigns PORT dynamically - use it if available
    port = int(os.getenv("PORT", settings.API_PORT))

    uvicorn.run(
        "server:app",
        host=settings.API_HOST,
        port=port,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
