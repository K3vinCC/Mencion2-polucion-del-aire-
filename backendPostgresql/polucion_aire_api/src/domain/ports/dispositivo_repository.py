from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from src.domain.entities.dispositivo import Dispositivo

class IDispositivoRepository(ABC):
    """Interfaz para el repositorio de dispositivos"""
    
    @abstractmethod
    def crear(self, dispositivo: Dispositivo) -> Dispositivo:
        """Crea un nuevo dispositivo"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Dispositivo]:
        """Obtiene un dispositivo por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_id_hardware(self, id_hardware: str) -> Optional[Dispositivo]:
        """Obtiene un dispositivo por su ID de hardware"""
        pass
    
    @abstractmethod
    def actualizar_estado(self, id: int, estado: str, ultima_vez_visto: datetime) -> bool:
        """Actualiza el estado y última vez visto de un dispositivo"""
        pass
    
    @abstractmethod
    def listar_por_sala(self, sala_id: int) -> List[Dispositivo]:
        """Lista todos los dispositivos en una sala"""
        pass
    
    @abstractmethod
    def listar_desconectados(self) -> List[Dispositivo]:
        """Lista todos los dispositivos desconectados"""
        pass