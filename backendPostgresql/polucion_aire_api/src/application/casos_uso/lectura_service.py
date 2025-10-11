from src.domain.ports.lectura_calidad_aire_repository import ILecturaCalidadAireRepository
from src.domain.ports.notificacion_service import INotificacionService
from src.domain.entities.lectura_calidad_aire import LecturaCalidadAire
from typing import List
import inject

class LecturaService:
    """Servicio de aplicación para gestionar lecturas de calidad del aire"""
    
    @inject.autoparams()
    def __init__(
        self,
        lectura_repository: ILecturaCalidadAireRepository,
        notificacion_service: INotificacionService
    ):
        self.lectura_repository = lectura_repository
        self.notificacion_service = notificacion_service
    
    def registrar_lectura(self, lectura: LecturaCalidadAire) -> LecturaCalidadAire:
        """
        Registra una nueva lectura y notifica si es necesario
        """
        # Guardar la lectura
        lectura_guardada = self.lectura_repository.crear(lectura)
        
        # Si la lectura requiere acción, notificar
        if lectura_guardada.requiere_accion():
            # Aquí se podría implementar la lógica para obtener el chat_id del conserje
            # y los detalles de la sala para la notificación
            pass
        
        return lectura_guardada
    
    def obtener_ultimas_lecturas(self, dispositivo_id: int, limite: int = 10) -> List[LecturaCalidadAire]:
        """
        Obtiene las últimas lecturas de un dispositivo
        """
        return self.lectura_repository.obtener_ultimas_lecturas(dispositivo_id, limite)