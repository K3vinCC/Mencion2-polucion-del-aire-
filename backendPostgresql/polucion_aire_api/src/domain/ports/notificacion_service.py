from abc import ABC, abstractmethod

class INotificacionService(ABC):
    """Interfaz para el servicio de notificaciones"""
    
    @abstractmethod
    def notificar_limpiador(
        self,
        telegram_chat_id: str,
        sala_nombre: str,
        edificio_nombre: str,
        nivel_calidad: str,
        asignacion_id: int
    ) -> bool:
        """
        Envía una notificación a un limpiador via Telegram
        """
        pass
    
    @abstractmethod
    def notificar_dispositivo_desconectado(
        self,
        admin_chat_id: str,
        dispositivo_id: str,
        sala_nombre: str,
        tiempo_desconectado: str
    ) -> bool:
        """
        Notifica a un administrador que un dispositivo está desconectado
        """
        pass