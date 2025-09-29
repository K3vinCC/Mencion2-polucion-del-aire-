# src/domain/ports/lectura_calidad_aire_repository.py
from abc import ABC, abstractmethod

class ILecturaCalidadAireRepository(ABC):
    """
    Interfaz para el Repositorio de Lecturas de Calidad del Aire.
    """

    @abstractmethod
    def save(self, lectura):
        """Guarda una nueva lectura en la base de datos."""
        pass

    @abstractmethod
    def find_by_id(self, lectura_id):
        """Busca una lectura por su ID."""
        pass

    @abstractmethod
    def get_by_dispositivo(self, id_dispositivo, limit=100):
        """Devuelve las últimas lecturas de un dispositivo."""
        pass

    @abstractmethod
    def get_by_edificio(self, id_edificio, limit=100):
        """Devuelve las últimas lecturas de todos los dispositivos de un edificio."""
        pass

    @abstractmethod
    def get_lecturas_recientes(self, horas=24):
        """Devuelve lecturas de las últimas N horas."""
        pass

    @abstractmethod
    def get_promedio_calidad(self, id_edificio, horas=24):
        """Calcula el promedio de calidad del aire en un edificio durante las últimas N horas."""
        pass