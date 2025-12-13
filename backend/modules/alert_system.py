"""
Sistema de Alertas Multi-Canal
Soporta: Email, Slack, Telegram, SMS (Twilio), Webhooks
"""
import asyncio
import aiohttp
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import logging

from config import settings

logger = logging.getLogger(__name__)


class AlertSystem:
    """
    Sistema centralizado de alertas
    """

    def __init__(self):
        self.alert_history: List[Dict] = []
        self.rate_limiter: Dict[str, datetime] = {}

    async def send_alert(
        self,
        level: str,  # "critical", "warning", "info"
        title: str,
        message: str,
        campaign_id: Optional[str] = None,
        channels: Optional[Dict] = None,
        screenshot_path: Optional[str] = None
    ):
        """
        Enviar alerta a múltiples canales

        Args:
            level: Nivel de alerta
            title: Título de la alerta
            message: Mensaje detallado
            campaign_id: ID de campaña relacionada
            channels: Dict con canales a usar {email: [...], slack: bool, telegram: bool}
            screenshot_path: Path opcional a screenshot
        """
        # Prevenir spam con rate limiting
        if self._is_rate_limited(campaign_id, level):
            logger.debug(f"Alerta rate-limited para {campaign_id}")
            return

        alert_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "title": title,
            "message": message,
            "campaign_id": campaign_id
        }

        self.alert_history.append(alert_data)
        logger.info(f"[{level.upper()}] {title}")

        # Determinar canales a usar
        if channels is None:
            channels = {}

        # Enviar a cada canal asíncronamente
        tasks = []

        # Email
        if channels.get("email"):
            emails = channels["email"] if isinstance(channels["email"], list) else []
            if emails:
                tasks.append(self._send_email(emails, title, message, level, screenshot_path))

        # Slack
        if channels.get("slack") and settings.SLACK_WEBHOOK_URL:
            tasks.append(self._send_slack(title, message, level))

        # Telegram
        if channels.get("telegram") and settings.TELEGRAM_BOT_TOKEN:
            tasks.append(self._send_telegram(title, message, level, screenshot_path))

        # SMS (solo para críticos)
        if level == "critical" and channels.get("sms") and settings.TWILIO_ACCOUNT_SID:
            tasks.append(self._send_sms(title, message))

        # Ejecutar todos los envíos en paralelo
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Log resultados
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Error enviando alerta: {result}")

    def _is_rate_limited(self, campaign_id: Optional[str], level: str) -> bool:
        """
        Rate limiting para prevenir spam de alertas

        Reglas:
        - Critical: sin límite
        - Warning: máximo 1 cada 30 minutos por campaña
        - Info: máximo 1 cada 2 horas por campaña
        """
        if level == "critical":
            return False

        if not campaign_id:
            return False

        key = f"{campaign_id}_{level}"
        last_alert = self.rate_limiter.get(key)

        if last_alert is None:
            self.rate_limiter[key] = datetime.utcnow()
            return False

        # Calcular tiempo desde última alerta
        time_diff = (datetime.utcnow() - last_alert).total_seconds()

        # Límites por nivel
        limits = {
            "warning": 30 * 60,  # 30 minutos
            "info": 2 * 60 * 60  # 2 horas
        }

        if time_diff < limits.get(level, 0):
            return True

        # Actualizar timestamp
        self.rate_limiter[key] = datetime.utcnow()
        return False

    async def _send_email(
        self,
        recipients: List[str],
        subject: str,
        body: str,
        level: str,
        screenshot_path: Optional[str] = None
    ):
        """Enviar email usando SMTP o SendGrid"""
        try:
            # Si hay SendGrid configurado, usarlo
            if settings.SENDGRID_API_KEY:
                await self._send_email_sendgrid(recipients, subject, body, screenshot_path)
            else:
                await self._send_email_smtp(recipients, subject, body, screenshot_path)

            logger.info(f"Email enviado a {len(recipients)} destinatarios")

        except Exception as e:
            logger.error(f"Error enviando email: {e}")
            raise

    async def _send_email_smtp(
        self,
        recipients: List[str],
        subject: str,
        body: str,
        screenshot_path: Optional[str] = None
    ):
        """Enviar email usando SMTP tradicional"""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"[Ad-Inspector] {subject}"
        msg['From'] = settings.SMTP_FROM_EMAIL
        msg['To'] = ', '.join(recipients)

        # Crear HTML con estilo
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: #1e293b; color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
                    .content {{ background: #f8fafc; padding: 20px; border-radius: 0 0 8px 8px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #64748b; font-size: 12px; }}
                    pre {{ background: #e2e8f0; padding: 10px; border-radius: 4px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>🤖 Ad-Inspector Bot</h2>
                        <p>{subject}</p>
                    </div>
                    <div class="content">
                        <pre>{body}</pre>
                    </div>
                    <div class="footer">
                        <p>Enviado desde Ad-Inspector Bot • {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                    </div>
                </div>
            </body>
        </html>
        """

        msg.attach(MIMEText(body, 'plain'))
        msg.attach(MIMEText(html, 'html'))

        # Adjuntar screenshot si existe
        if screenshot_path and Path(screenshot_path).exists():
            with open(screenshot_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-Disposition', 'attachment', filename='screenshot.png')
                msg.attach(img)

        # Enviar
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

    async def _send_email_sendgrid(
        self,
        recipients: List[str],
        subject: str,
        body: str,
        screenshot_path: Optional[str] = None
    ):
        """Enviar email usando SendGrid API"""
        # TODO: Implementar SendGrid
        logger.warning("SendGrid no implementado aún, usando SMTP")
        await self._send_email_smtp(recipients, subject, body, screenshot_path)

    async def _send_slack(self, title: str, message: str, level: str):
        """Enviar alerta a Slack usando webhook"""
        # Colores por nivel
        colors = {
            "critical": "#ef4444",
            "warning": "#f59e0b",
            "info": "#3b82f6"
        }

        # Iconos por nivel
        icons = {
            "critical": "🚨",
            "warning": "⚠️",
            "info": "ℹ️"
        }

        payload = {
            "attachments": [
                {
                    "color": colors.get(level, "#3b82f6"),
                    "title": f"{icons.get(level, '')} {title}",
                    "text": message,
                    "footer": "Ad-Inspector Bot",
                    "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                    "ts": int(datetime.utcnow().timestamp())
                }
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    settings.SLACK_WEBHOOK_URL,
                    json=payload
                ) as response:
                    if response.status == 200:
                        logger.info("Alerta enviada a Slack")
                    else:
                        logger.error(f"Error Slack: {response.status}")

        except Exception as e:
            logger.error(f"Error enviando a Slack: {e}")
            raise

    async def _send_telegram(
        self,
        title: str,
        message: str,
        level: str,
        screenshot_path: Optional[str] = None
    ):
        """Enviar alerta a Telegram"""
        # Iconos por nivel
        icons = {
            "critical": "🚨",
            "warning": "⚠️",
            "info": "ℹ️"
        }

        text = f"{icons.get(level, '')} *{title}*\n\n{message}"

        # URL de Telegram Bot API
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        logger.info("Alerta enviada a Telegram")

                        # Enviar screenshot si existe
                        if screenshot_path and Path(screenshot_path).exists():
                            await self._send_telegram_photo(screenshot_path)
                    else:
                        logger.error(f"Error Telegram: {response.status}")

        except Exception as e:
            logger.error(f"Error enviando a Telegram: {e}")
            raise

    async def _send_telegram_photo(self, photo_path: str):
        """Enviar foto a Telegram"""
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendPhoto"

        try:
            async with aiohttp.ClientSession() as session:
                with open(photo_path, 'rb') as photo:
                    data = aiohttp.FormData()
                    data.add_field('chat_id', settings.TELEGRAM_CHAT_ID)
                    data.add_field('photo', photo)

                    async with session.post(url, data=data) as response:
                        if response.status == 200:
                            logger.debug("Screenshot enviado a Telegram")

        except Exception as e:
            logger.error(f"Error enviando foto a Telegram: {e}")

    async def _send_sms(self, title: str, message: str):
        """Enviar SMS usando Twilio (solo para alertas críticas)"""
        # TODO: Implementar Twilio
        logger.warning("SMS/Twilio no implementado aún")
        pass

    def get_alert_history(self, limit: int = 100) -> List[Dict]:
        """Obtener historial de alertas"""
        return self.alert_history[-limit:]

    def clear_history(self):
        """Limpiar historial de alertas"""
        self.alert_history = []
        logger.info("Historial de alertas limpiado")
