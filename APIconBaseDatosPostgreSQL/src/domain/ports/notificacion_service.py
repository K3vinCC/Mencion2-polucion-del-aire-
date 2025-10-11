# src/domain/ports/notificacion_service.py
"""
Puerto (Interfaz) para el servicio de notificaciones.
Define el contrato que deben implementar todos los adaptadores de notificaciones.
"""

from abc import ABC, abstractmethod
from typing import Optional


class INotificacionService(ABC):
    """
    Interfaz del servicio de notificaciones.

    Define las operaciones de notificación que cualquier adaptador
    (Telegram, Email, SMS, etc.) debe implementar.
    """

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
            dict: Datos del resumen diario con estadísticas de calidad del aire,
                  dispositivos conectados, asignaciones completadas, etc.
        """
        pass

    @abstractmethod
    def validar_configuracion(self) -> bool:
        """
        Valida que la configuración del servicio de notificaciones sea correcta.

        Returns:
            bool: True si la configuración es válida, False en caso contrario
        """
        pass

    @abstractmethod
    def obtener_estadisticas_envio(self) -> dict:
        """
        Obtiene estadísticas de envío de notificaciones.

        Returns:
            dict: Estadísticas como número total de envíos, tasa de éxito,
                  tipos de notificaciones enviadas, etc.
        """
        pass