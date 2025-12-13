"""
Análisis inteligente con Google Gemini AI
Analiza errores y proporciona insights accionables
"""
import logging
from typing import Dict, List, Optional
import google.generativeai as genai
from config import settings

logger = logging.getLogger(__name__)

# Configurar Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)


async def analyze_error_with_ai(campaign: Dict, result: Dict) -> str:
    """
    Analiza errores de una campaña y proporciona recomendaciones

    Args:
        campaign: Configuración de la campaña
        result: Resultado de la verificación

    Returns:
        Análisis detallado en texto
    """
    if not settings.ENABLE_AI_ANALYSIS or not settings.GEMINI_API_KEY:
        return "Análisis AI deshabilitado"

    try:
        model = genai.GenerativeModel(settings.GEMINI_MODEL)

        # Construir prompt
        prompt = f"""
Eres un experto en debugging de páginas web y optimización de campañas publicitarias.

**Campaña:** {campaign['name']}
**URL:** {result['url']}
**Estado:** {'ÉXITO' if result['success'] else 'FALLIDA'}
**Tiempo de carga:** {result['load_time']}s

**Errores encontrados:**
{chr(10).join(f"- {err}" for err in result['errors'])}

**Elementos faltantes:**
{', '.join(result['elements_missing']) if result['elements_missing'] else 'Ninguno'}

**Acciones ejecutadas:**
{chr(10).join(f"- {action.get('description', action.get('type'))}" for action in campaign.get('actions', []))}

Por favor, proporciona:

1. **Diagnóstico:** ¿Qué está causando los errores?
2. **Impacto:** ¿Cómo afecta esto a la conversión y ROI?
3. **Solución:** Pasos específicos para resolver los problemas
4. **Prevención:** Cómo evitar que esto vuelva a suceder

Sé conciso pero completo. Máximo 300 palabras.
"""

        # Generar respuesta
        response = model.generate_content(prompt)
        analysis = response.text

        logger.info(f"Análisis AI generado para {campaign['id']}")
        return analysis

    except Exception as e:
        logger.error(f"Error en análisis AI: {e}")
        return f"Error generando análisis: {str(e)}"


async def generate_dashboard_insight(campaigns: List[Dict], avg_load_time: float) -> str:
    """
    Genera insight general del dashboard

    Args:
        campaigns: Lista de campañas con sus estados
        avg_load_time: Tiempo de carga promedio

    Returns:
        Insight en texto
    """
    if not settings.ENABLE_AI_ANALYSIS or not settings.GEMINI_API_KEY:
        return "Análisis AI deshabilitado"

    try:
        model = genai.GenerativeModel(settings.GEMINI_MODEL)

        # Estadísticas
        total = len(campaigns)
        active = sum(1 for c in campaigns if c.get('status') == 'active')
        errors = sum(1 for c in campaigns if c.get('status') == 'error')

        # Campañas con error
        error_campaigns = [c for c in campaigns if c.get('status') == 'error']
        error_details = "\n".join([
            f"- {c['name']}: {', '.join(c.get('errors', []))[:100]}"
            for c in error_campaigns[:3]
        ])

        prompt = f"""
Eres un analista de marketing digital experto.

**Resumen de campañas:**
- Total: {total}
- Activas y saludables: {active}
- Con errores críticos: {errors}
- Tiempo de carga promedio: {avg_load_time:.2f}s

**Campañas con problemas:**
{error_details if error_details else 'Ninguna'}

Proporciona un insight breve (máximo 150 palabras) sobre:
1. Estado general de las campañas
2. Problemas más críticos a resolver
3. Recomendación principal para mejorar el ROI

Sé directo y accionable.
"""

        response = model.generate_content(prompt)
        insight = response.text

        logger.info("Dashboard insight generado")
        return insight

    except Exception as e:
        logger.error(f"Error generando insight: {e}")
        return f"Error: {str(e)}"


async def analyze_campaign_error(campaign: Dict) -> str:
    """
    Análisis específico de error de campaña (llamado desde frontend)

    Args:
        campaign: Datos de campaña con errores

    Returns:
        Análisis técnico detallado
    """
    if not settings.ENABLE_AI_ANALYSIS or not settings.GEMINI_API_KEY:
        return "Análisis AI no disponible. Configure GEMINI_API_KEY."

    try:
        model = genai.GenerativeModel(settings.GEMINI_MODEL)

        errors = campaign.get('errors', [])
        load_time = campaign.get('loadTime', 0)
        url = campaign.get('url', '')

        prompt = f"""
Eres un ingeniero de software senior especializado en debugging web.

**Campaña:** {campaign.get('name')}
**URL:** {url}
**Tiempo de carga:** {load_time}s
**Errores:**
{chr(10).join(f"• {err}" for err in errors)}

Proporciona:

1. **Causa raíz:** Diagnóstico técnico del problema
2. **Código de ejemplo:** Si aplica, muestra código para resolver el issue
3. **Pasos a seguir:** Lista numerada de acciones inmediatas
4. **Impacto estimado:** Cuánto presupuesto se está perdiendo por este error

Sé técnico pero claro. Máximo 250 palabras.
"""

        response = model.generate_content(prompt)
        analysis = response.text

        logger.info(f"Análisis de error generado para {campaign.get('id')}")
        return analysis

    except Exception as e:
        logger.error(f"Error en análisis de campaña: {e}")
        return f"No se pudo generar análisis: {str(e)}"


async def suggest_optimizations(campaign: Dict, performance_data: Dict) -> str:
    """
    Sugerir optimizaciones basadas en datos de performance

    Args:
        campaign: Configuración de campaña
        performance_data: Métricas de rendimiento

    Returns:
        Sugerencias de optimización
    """
    if not settings.ENABLE_AI_ANALYSIS or not settings.GEMINI_API_KEY:
        return "Análisis AI deshabilitado"

    try:
        model = genai.GenerativeModel(settings.GEMINI_MODEL)

        prompt = f"""
Eres un experto en optimización de conversión (CRO).

**Campaña:** {campaign['name']}
**URL:** {campaign['url']}

**Métricas actuales:**
- Tiempo de carga: {performance_data.get('load_time', 0)}s
- Tasa de conversión: {performance_data.get('conversion_rate', 0)}%
- Disponibilidad: {performance_data.get('uptime', 100)}%

Sugiere 3-5 optimizaciones concretas para:
1. Mejorar la velocidad de carga
2. Aumentar la tasa de conversión
3. Reducir fricción en el embudo

Cada sugerencia debe ser específica y accionable, no genérica.
Máximo 200 palabras.
"""

        response = model.generate_content(prompt)
        suggestions = response.text

        logger.info(f"Optimizaciones sugeridas para {campaign['id']}")
        return suggestions

    except Exception as e:
        logger.error(f"Error sugiriendo optimizaciones: {e}")
        return f"Error: {str(e)}"
