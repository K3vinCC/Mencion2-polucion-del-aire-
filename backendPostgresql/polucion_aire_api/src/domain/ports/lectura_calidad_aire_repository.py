from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from datetime import datetime
from src.domain.entities.lectura_calidad_aire import LecturaCalidadAire

class ILecturaCalidadAireRepository(ABC):
    """Interfaz para el repositorio de lecturas de calidad del aire"""
    
    @abstractmethod
    def crear(self, lectura: LecturaCalidadAire) -> LecturaCalidadAire:
        """Registra una nueva lectura"""
        pass
    
    @abstractmethod
    def obtener_ultimas_lecturas(self, dispositivo_id: int, limite: int = 10) -> List[LecturaCalidadAire]:
        """Obtiene las últimas N lecturas de un dispositivo"""
        pass
    
    @abstractmethod
    def obtener_promedio_periodo(
        self,
        dispositivo_id: int,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> Tuple[float, float, float]:
        """
        Obtiene el promedio de PM1, PM2.5 y PM10 para un período
        Retorna una tupla con (pm1_avg, pm2_5_avg, pm10_avg)
        """
        pass
    
    @abstractmethod
    def obtener_lecturas_criticas(
        self,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> List[LecturaCalidadAire]:
        """
        Obtiene las lecturas que requieren acción en un período
        """
        pass