"""
Configuración centralizada del Ad-Inspector Bot
"""
import os
from pathlib import Path
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Configuración principal de la aplicación"""

    # General
    APP_NAME: str = "Ad-Inspector Bot"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent
    LOGS_DIR: Path = BASE_DIR / "logs"
    SCREENSHOTS_DIR: Path = BASE_DIR / "screenshots"
    REPORTS_DIR: Path = BASE_DIR / "reports"

    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./inspector.db",
        env="DATABASE_URL"
    )
    DB_ECHO: bool = Field(default=False, env="DB_ECHO")

    @validator("DATABASE_URL", pre=True)
    def fix_database_url_typo(cls, v):
        """Auto-fix common typo: qlite -> sqlite"""
        if isinstance(v, str) and v.startswith("qlite://"):
            # Fix typo: qlite -> sqlite
            return v.replace("qlite://", "sqlite://", 1)
        return v

    # Redis (para cache y Celery)
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )

    # API Configuration
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    API_PREFIX: str = "/api/v1"
    # Use Union to prevent automatic JSON parsing
    CORS_ORIGINS: Union[str, List[str]] = Field(
        default="http://localhost:5173,http://localhost:5174,http://localhost:3000,https://proyecto-inspector.vercel.app",
        env="CORS_ORIGINS"
    )

    @validator("CORS_ORIGINS", pre=True, always=True)
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from string or list"""
        # If already a list, return it
        if isinstance(v, list):
            return v
        # If string, split by comma
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        # Fallback
        return ["http://localhost:5173"]

    # Scheduler Configuration
    CHECK_INTERVAL_MINUTES: int = Field(default=10, env="CHECK_INTERVAL_MINUTES")
    MAX_CONCURRENT_CHECKS: int = Field(default=5, env="MAX_CONCURRENT_CHECKS")
    RETRY_FAILED_CHECKS: bool = Field(default=True, env="RETRY_FAILED_CHECKS")
    MAX_RETRY_ATTEMPTS: int = Field(default=3, env="MAX_RETRY_ATTEMPTS")

    # Browser Configuration
    HEADLESS_BROWSER: bool = Field(default=True, env="HEADLESS_BROWSER")
    BROWSER_TYPE: str = Field(default="chromium", env="BROWSER_TYPE")  # chromium, firefox, webkit
    BROWSER_TIMEOUT: int = Field(default=30000, env="BROWSER_TIMEOUT")  # milliseconds
    USER_AGENT: Optional[str] = Field(default=None, env="USER_AGENT")

    # Performance Thresholds
    MAX_LOAD_TIME_SECONDS: float = Field(default=3.5, env="MAX_LOAD_TIME_SECONDS")
    MIN_LIGHTHOUSE_SCORE: int = Field(default=70, env="MIN_LIGHTHOUSE_SCORE")

    # AI Configuration (Gemini)
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-pro", env="GEMINI_MODEL")
    ENABLE_AI_ANALYSIS: bool = Field(default=True, env="ENABLE_AI_ANALYSIS")

    # OpenAI (opcional)
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4", env="OPENAI_MODEL")

    # Email Notifications
    SMTP_HOST: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: str = Field(default="", env="SMTP_USER")
    SMTP_PASSWORD: str = Field(default="", env="SMTP_PASSWORD")
    SMTP_FROM_EMAIL: str = Field(default="noreply@ad-inspector.dev", env="SMTP_FROM_EMAIL")

    # SendGrid (alternativa a SMTP)
    SENDGRID_API_KEY: Optional[str] = Field(default=None, env="SENDGRID_API_KEY")

    # Slack
    SLACK_WEBHOOK_URL: Optional[str] = Field(default=None, env="SLACK_WEBHOOK_URL")
    SLACK_BOT_TOKEN: Optional[str] = Field(default=None, env="SLACK_BOT_TOKEN")
    SLACK_CHANNEL: str = Field(default="#alerts", env="SLACK_CHANNEL")

    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(default=None, env="TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: Optional[str] = Field(default=None, env="TELEGRAM_CHAT_ID")

    # Twilio (SMS)
    TWILIO_ACCOUNT_SID: Optional[str] = Field(default=None, env="TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = Field(default=None, env="TWILIO_AUTH_TOKEN")
    TWILIO_FROM_NUMBER: Optional[str] = Field(default=None, env="TWILIO_FROM_NUMBER")

    # CRM Integrations
    # HubSpot
    HUBSPOT_API_KEY: Optional[str] = Field(default=None, env="HUBSPOT_API_KEY")
    HUBSPOT_PORTAL_ID: Optional[str] = Field(default=None, env="HUBSPOT_PORTAL_ID")

    # Salesforce
    SALESFORCE_USERNAME: Optional[str] = Field(default=None, env="SALESFORCE_USERNAME")
    SALESFORCE_PASSWORD: Optional[str] = Field(default=None, env="SALESFORCE_PASSWORD")
    SALESFORCE_SECURITY_TOKEN: Optional[str] = Field(default=None, env="SALESFORCE_SECURITY_TOKEN")

    # Monitoring & Analytics
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    ENABLE_PROMETHEUS: bool = Field(default=False, env="ENABLE_PROMETHEUS")

    # Security
    SECRET_KEY: str = Field(
        default="change-me-in-production-use-strong-random-key",
        env="SECRET_KEY"
    )
    API_KEY_HEADER: str = "X-API-Key"

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")

    @validator("LOGS_DIR", "SCREENSHOTS_DIR", "REPORTS_DIR", pre=True, always=True)
    def create_directories(cls, v):
        """Crear directorios si no existen"""
        path = Path(v) if isinstance(v, str) else v
        path.mkdir(parents=True, exist_ok=True)
        return path

    @validator("GEMINI_API_KEY")
    def validate_gemini_key(cls, v, values):
        """Validar que Gemini API key esté presente si AI está habilitado"""
        # Solo validar en development - en production puede estar vacío si AI está deshabilitado
        if values.get("ENABLE_AI_ANALYSIS") and not v:
            if values.get("ENVIRONMENT") == "development":
                raise ValueError("GEMINI_API_KEY es requerido cuando ENABLE_AI_ANALYSIS=True")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton de configuración
settings = Settings()


# Viewports predefinidos
VIEWPORTS = {
    "desktop": {"width": 1920, "height": 1080},
    "laptop": {"width": 1366, "height": 768},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 667},
    "mobile_large": {"width": 414, "height": 896},
}


# User Agents realistas
USER_AGENTS = {
    "desktop": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "mobile": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "tablet": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
}


# Status codes considerados como error
HTTP_ERROR_CODES = [400, 401, 403, 404, 500, 502, 503, 504]


# Elementos críticos comunes en landing pages
COMMON_CRITICAL_ELEMENTS = [
    "form",
    "button[type='submit']",
    "input[type='email']",
    ".cta-button",
    "#contact-form",
    ".signup-form",
]


def get_viewport(viewport_name: str) -> dict:
    """Obtener configuración de viewport por nombre"""
    return VIEWPORTS.get(viewport_name.lower(), VIEWPORTS["desktop"])


def get_user_agent(device_type: str) -> str:
    """Obtener user agent por tipo de dispositivo"""
    return USER_AGENTS.get(device_type.lower(), USER_AGENTS["desktop"])
