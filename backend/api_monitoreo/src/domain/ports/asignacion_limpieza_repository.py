# src/domain/ports/asignacion_limpieza_repository.py
from abc import ABC, abstractmethod

class IAsignacionLimpiezaRepository(ABC):
    """
    Interfaz para el Repositorio de Asignaciones de Limpieza.
    """

    @abstractmethod
    def save(self, asignacion):
        """Guarda una nueva asignación en la base de datos."""
        pass

    @abstractmethod
    def find_by_id(self, asignacion_id):
        """Busca una asignación por su ID."""
        pass

    @abstractmethod
    def get_by_usuario(self, id_usuario):
        """Devuelve todas las asignaciones de un usuario."""
        pass

    @abstractmethod
    def get_pendientes(self):
        """Devuelve todas las asignaciones pendientes."""
        pass

    @abstractmethod
    def get_by_estado(self, estado):
        """Devuelve asignaciones filtradas por estado."""
        pass

    @abstractmethod
    def update_estado(self, asignacion_id, estado, fecha_completado=None):
        """Actualiza el estado de una asignación."""
        pass