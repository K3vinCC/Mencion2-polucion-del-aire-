# src/infrastructure/services/telegram_service.py
"""
Servicio de notificaciones usando Telegram Bot API.
Implementa el envío de notificaciones a través de Telegram.
"""

import logging
from typing import Optional, Dict, Any
import requests
from datetime import datetime

from src.config import get_config
from src.domain.ports.notificacion_service import INotificacionService


logger = logging.getLogger(__name__)


class TelegramService(INotificacionService):
    """
    Servicio de notificaciones usando Telegram Bot API.

    Implementa el envío de alertas, asignaciones y reportes a través de Telegram.
    """

    def __init__(self):
        """Inicializa el servicio con la configuración de Telegram."""
        self.config = get_config()
        self.bot_token = self.config.TELEGRAM_BOT_TOKEN
        self.chat_id = self.config.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

        # Verificar configuración al inicializar
        self._config_valid = self.validar_configuracion()

    def _send_message(self, message: str, parse_mode: str = 'HTML') -> bool:
        """
        Envía un mensaje a través de Telegram.

        Args:
            message: Contenido del mensaje
            parse_mode: Modo de parseo ('HTML', 'Markdown', etc.)

        Returns:
            bool: True si se envió correctamente
        """
        if not self._config_valid:
            logger.warning("Configuración de Telegram no válida, mensaje no enviado")
            return False

        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode,
                'disable_web_page_preview': True
            }

            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            result = response.json()
            if result.get('ok'):
                logger.info(f"Mensaje enviado correctamente a chat {self.chat_id}")
                return True
            else:
                logger.error(f"Error al enviar mensaje: {result.get('description')}")
                return False

        except requests.RequestException as e:
            logger.error(f"Error de conexión al enviar mensaje: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado al enviar mensaje: {str(e)}")
            return False

    def _format_air_quality_level(self, level: str) -> str:
        """
        Formatea el nivel de calidad del aire con emojis apropiados.

        Args:
            level: Nivel de calidad del aire

        Returns:
            str: Nivel formateado con emoji
        """
        level_emojis = {
            'BUENO': '🟢 BUENO',
            'MODERADO': '🟡 MODERADO',
            'INSALUBRE_GRUPOS_SENSIBLES': '🟠 INSALUBRE PARA GRUPOS SENSIBLES',
            'INSALUBRE': '🔴 INSALUBRE',
            'NOCIVO': '💀 NOCIVO'
        }
        return level_emojis.get(level, f'⚪ {level}')

    def enviar_alerta_calidad_aire(
        self,
        usuario_id: int,
        sala_nombre: str,
        nivel_calidad: str,
        valores_pm: dict,
        mensaje_adicional: Optional[str] = None
    ) -> bool:
        """
        Envía una alerta de calidad del aire deficiente a un usuario.

        Args:
            usuario_id: ID del usuario destinatario
            sala_nombre: Nombre de la sala con problemas
            nivel_calidad: Nivel de calidad ('NOCIVO', 'INSALUBRE', etc.)
            valores_pm: Diccionario con valores de PM {'pm1': X, 'pm2_5': Y, 'pm10': Z}
            mensaje_adicional: Mensaje adicional opcional

        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            nivel_formateado = self._format_air_quality_level(nivel_calidad)

            message = f"""
🚨 <b>ALERTA DE CALIDAD DEL AIRE</b> 🚨

📍 <b>Ubicación:</b> {sala_nombre}
📊 <b>Nivel de Calidad:</b> {nivel_formateado}

<b>Valores medidos:</b>
• PM1: {valores_pm.get('pm1', 'N/A')} μg/m³
• PM2.5: {valores_pm.get('pm2_5', 'N/A')} μg/m³
• PM10: {valores_pm.get('pm10', 'N/A')} μg/m³

⏰ <b>Hora:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 <b>Usuario ID:</b> {usuario_id}
"""

            if mensaje_adicional:
                message += f"\n💬 <b>Nota:</b> {mensaje_adicional}"

            message += "\n\n🔧 <i>Se recomienda ventilación inmediata</i>"

            return self._send_message(message)

        except Exception as e:
            logger.error(f"Error al enviar alerta de calidad del aire: {str(e)}")
            return False

    def enviar_asignacion_limpieza(
        self,
        usuario_id: int,
        sala_nombre: str,
        edificio_nombre: str,
        mensaje_instrucciones: str
    ) -> bool:
        """
        Envía una notificación de asignación de tarea de limpieza.

        Args:
            usuario_id: ID del usuario limpiador
            sala_nombre: Nombre de la sala a limpiar
            edificio_nombre: Nombre del edificio
            mensaje_instrucciones: Instrucciones específicas para la limpieza

        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            message = f"""
🧹 <b>NUEVA ASIGNACIÓN DE LIMPIEZA</b> 🧹

🏢 <b>Edificio:</b> {edificio_nombre}
📍 <b>Sala:</b> {sala_nombre}

📋 <b>Instrucciones:</b>
{mensaje_instrucciones}

⏰ <b>Fecha de asignación:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 <b>Limpiador ID:</b> {usuario_id}

✅ <i>Por favor confirme recepción y complete la tarea lo antes posible</i>
"""

            return self._send_message(message)

        except Exception as e:
            logger.error(f"Error al enviar asignación de limpieza: {str(e)}")
            return False

    def enviar_recordatorio_mantenimiento(
        self,
        usuario_id: int,
        dispositivo_id: int,
        mac_address: str,
        dias_sin_mantenimiento: int
    ) -> bool:
        """
        Envía un recordatorio de mantenimiento de dispositivo.

        Args:
            usuario_id: ID del usuario administrador
            dispositivo_id: ID del dispositivo que necesita mantenimiento
            mac_address: Dirección MAC del dispositivo
            dias_sin_mantenimiento: Días transcurridos desde el último mantenimiento

        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            message = f"""
🔧 <b>RECORDATORIO DE MANTENIMIENTO</b> 🔧

📱 <b>Dispositivo ID:</b> {dispositivo_id}
🔗 <b>MAC Address:</b> {mac_address}

⏳ <b>Días sin mantenimiento:</b> {dias_sin_mantenimiento}

⚠️ <b>Recomendación:</b> Realizar mantenimiento preventivo del dispositivo
• Verificar sensores
• Limpiar filtros
• Calibrar mediciones
• Actualizar firmware si es necesario

⏰ <b>Fecha:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 <b>Administrador ID:</b> {usuario_id}
"""

            return self._send_message(message)

        except Exception as e:
            logger.error(f"Error al enviar recordatorio de mantenimiento: {str(e)}")
            return False

    def enviar_reporte_diario(
        self,
        usuario_id: int,
        universidad_nombre: str,
        resumen_datos: dict
    ) -> bool:
        """
        Envía un reporte diario con resumen de datos.

        Args:
            usuario_id: ID del usuario destinatario
            universidad_nombre: Nombre de la universidad
            resumen_datos: Diccionario con estadísticas diarias

        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            dispositivos_conectados = resumen_datos.get('dispositivos_conectados', 0)
            dispositivos_desconectados = resumen_datos.get('dispositivos_desconectados', 0)
            total_lecturas = resumen_datos.get('total_lecturas', 0)
            asignaciones_completadas = resumen_datos.get('asignaciones_completadas', 0)
            alertas_enviadas = resumen_datos.get('alertas_enviadas', 0)

            calidad_promedio = resumen_datos.get('calidad_promedio', 'N/A')
            if isinstance(calidad_promedio, dict):
                calidad_promedio = calidad_promedio.get('nivel', 'N/A')

            message = f"""
📊 <b>REPORTE DIARIO - {universidad_nombre}</b> 📊

📅 <b>Fecha:</b> {datetime.now().strftime('%Y-%m-%d')}

<b>📱 Dispositivos:</b>
• Conectados: {dispositivos_conectados}
• Desconectados: {dispositivos_desconectados}
• Total: {dispositivos_conectados + dispositivos_desconectados}

<b>📈 Mediciones:</b>
• Total de lecturas: {total_lecturas}
• Calidad promedio: {self._format_air_quality_level(calidad_promedio) if calidad_promedio != 'N/A' else 'N/A'}

<b>🧹 Limpieza:</b>
• Asignaciones completadas: {asignaciones_completadas}

<b>🚨 Alertas:</b>
• Alertas enviadas: {alertas_enviadas}

⏰ <b>Hora del reporte:</b> {datetime.now().strftime('%H:%M:%S')}
👤 <b>Usuario ID:</b> {usuario_id}
"""

            return self._send_message(message)

        except Exception as e:
            logger.error(f"Error al enviar reporte diario: {str(e)}")
            return False

    def validar_configuracion(self) -> bool:
        """
        Valida que la configuración del servicio de notificaciones sea correcta.

        Returns:
            bool: True si la configuración es válida, False en caso contrario
        """
        if not self.bot_token or not self.chat_id:
            logger.warning("Token de bot o Chat ID de Telegram no configurados")
            return False

        try:
            # Verificar que el bot token sea válido haciendo una petición simple
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            result = response.json()
            if result.get('ok'):
                logger.info("Configuración de Telegram validada correctamente")
                return True
            else:
                logger.error(f"Token de bot inválido: {result.get('description')}")
                return False

        except requests.RequestException as e:
            logger.error(f"Error de conexión al validar configuración: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado al validar configuración: {str(e)}")
            return False

    def obtener_estadisticas_envio(self) -> dict:
        """
        Obtiene estadísticas de envío de notificaciones.

        Returns:
            dict: Estadísticas como número total de envíos, tasa de éxito,
                  tipos de notificaciones enviadas, etc.
        """
        # En una implementación real, estas estadísticas se almacenarían en BD
        # Por ahora retornamos datos simulados
        return {
            'total_envios': 0,  # Se implementaría con contador en BD
            'envios_exitosos': 0,
            'envios_fallidos': 0,
            'tasa_exito': 0.0,
            'tipos_notificaciones': {
                'alertas_calidad_aire': 0,
                'asignaciones_limpieza': 0,
                'recordatorios_mantenimiento': 0,
                'reportes_diarios': 0
            },
            'ultimo_envio': None
        }