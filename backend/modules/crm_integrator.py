"""
Integración con CRMs (HubSpot, Salesforce)
Para validar que las conversiones se están registrando correctamente
"""
import logging
from typing import Dict, Optional
import aiohttp
from datetime import datetime
from config import settings

logger = logging.getLogger(__name__)


class CRMIntegrator:
    """Clase base para integraciones CRM"""

    async def send_test_lead(self, campaign_id: str, data: Dict) -> bool:
        """Enviar lead de prueba al CRM"""
        raise NotImplementedError


class HubSpotIntegrator(CRMIntegrator):
    """Integración con HubSpot"""

    def __init__(self):
        self.api_key = settings.HUBSPOT_API_KEY
        self.portal_id = settings.HUBSPOT_PORTAL_ID
        self.base_url = "https://api.hubapi.com"

    async def send_test_lead(self, campaign_id: str, data: Dict) -> bool:
        """
        Enviar contacto de prueba a HubSpot

        Args:
            campaign_id: ID de la campaña
            data: Datos del lead (email, name, etc.)

        Returns:
            True si fue exitoso
        """
        if not self.api_key:
            logger.warning("HubSpot API key no configurada")
            return False

        try:
            url = f"{self.base_url}/contacts/v1/contact"

            # Construir payload de HubSpot
            properties = []
            for key, value in data.items():
                properties.append({
                    "property": key,
                    "value": value
                })

            # Agregar metadata de test
            properties.extend([
                {
                    "property": "ad_inspector_test",
                    "value": "true"
                },
                {
                    "property": "campaign_id",
                    "value": campaign_id
                },
                {
                    "property": "test_timestamp",
                    "value": datetime.utcnow().isoformat()
                }
            ])

            payload = {"properties": properties}

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status in [200, 201]:
                        logger.info(f"Lead de prueba enviado a HubSpot: {data.get('email')}")
                        return True
                    else:
                        error = await response.text()
                        logger.error(f"Error HubSpot: {response.status} - {error}")
                        return False

        except Exception as e:
            logger.exception(f"Error enviando lead a HubSpot: {e}")
            return False

    async def verify_webhook(self, campaign_id: str) -> bool:
        """Verificar que webhook de HubSpot esté funcionando"""
        # TODO: Implementar verificación de webhook
        return True


class SalesforceIntegrator(CRMIntegrator):
    """Integración con Salesforce"""

    def __init__(self):
        self.username = settings.SALESFORCE_USERNAME
        self.password = settings.SALESFORCE_PASSWORD
        self.security_token = settings.SALESFORCE_SECURITY_TOKEN

    async def send_test_lead(self, campaign_id: str, data: Dict) -> bool:
        """Enviar lead de prueba a Salesforce"""
        if not all([self.username, self.password, self.security_token]):
            logger.warning("Credenciales de Salesforce no configuradas")
            return False

        try:
            # TODO: Implementar integración con Salesforce usando simple-salesforce
            logger.warning("Integración Salesforce pendiente de implementar")
            return False

        except Exception as e:
            logger.exception(f"Error enviando lead a Salesforce: {e}")
            return False


def get_crm_integrator(provider: str) -> Optional[CRMIntegrator]:
    """
    Factory para obtener integrador CRM

    Args:
        provider: "hubspot" o "salesforce"

    Returns:
        Instancia del integrador correspondiente
    """
    providers = {
        "hubspot": HubSpotIntegrator,
        "salesforce": SalesforceIntegrator
    }

    integrator_class = providers.get(provider.lower())

    if integrator_class:
        return integrator_class()

    logger.warning(f"Proveedor CRM desconocido: {provider}")
    return None
