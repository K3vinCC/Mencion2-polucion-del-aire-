import telegram
import os
from src.domain.ports.notificacion_service import INotificacionService

class TelegramNotificacionService(INotificacionService):
    """Implementación del servicio de notificaciones usando Telegram"""
    
    def __init__(self):
        self.bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    
    def notificar_limpiador(
        self,
        telegram_chat_id: str,
        sala_nombre: str,
        edificio_nombre: str,
        nivel_calidad: str,
        asignacion_id: int
    ) -> bool:
        try:
            mensaje = (
                f"🚨 NUEVA TAREA DE LIMPIEZA 🧹\n\n"
                f"Sala: {sala_nombre}\n"
                f"Edificio: {edificio_nombre}\n"
                f"Nivel de calidad del aire: {nivel_calidad}\n\n"
                f"Por favor, dirígete a la sala asignada lo antes posible.\n"
                f"ID de asignación: #{asignacion_id}"
            )
            
            self.bot.send_message(
                chat_id=telegram_chat_id,
                text=mensaje,
                parse_mode='HTML'
            )
            return True
        except Exception as e:
            print(f"Error al enviar notificación: {str(e)}")
            return False
    
    def notificar_dispositivo_desconectado(
        self,
        admin_chat_id: str,
        dispositivo_id: str,
        sala_nombre: str,
        tiempo_desconectado: str
    ) -> bool:
        try:
            mensaje = (
                f"⚠️ ALERTA: DISPOSITIVO DESCONECTADO ⚠️\n\n"
                f"Dispositivo ID: {dispositivo_id}\n"
                f"Sala: {sala_nombre}\n"
                f"Tiempo desconectado: {tiempo_desconectado}\n\n"
                f"Por favor, revise el estado del dispositivo."
            )
            
            self.bot.send_message(
                chat_id=admin_chat_id,
                text=mensaje,
                parse_mode='HTML'
            )
            return True
        except Exception as e:
            print(f"Error al enviar notificación: {str(e)}")
            return False