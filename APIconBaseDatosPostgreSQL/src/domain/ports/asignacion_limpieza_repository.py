# src/domain/ports/asignacion_limpieza_repository.py
"""
Puerto (Interfaz) para el repositorio de asignaciones de limpieza.
Define el contrato que deben implementar todos los adaptadores de persistencia.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.asignacion_limpieza import AsignacionLimpieza


class IAsignacionLimpiezaRepository(ABC):
    """
    Interfaz del repositorio de asignaciones de limpieza.

    Define las operaciones de persistencia que cualquier adaptador
    de base de datos debe implementar para manejar asignaciones de limpieza.
    """

    @abstractmethod
    def save(self, asignacion: AsignacionLimpieza) -> AsignacionLimpieza:
        """
        Guarda una nueva asignación de limpieza.

        Args:
            asignacion: La entidad AsignacionLimpieza a persistir

        Returns:
            AsignacionLimpieza: La entidad con su ID asignado
        """
        pass

    @abstractmethod
    def find_by_id(self, asignacion_id: int) -> Optional[AsignacionLimpieza]:
        """
        Busca una asignación por su ID.

        Args:
            asignacion_id: El ID de la asignación a buscar

        Returns:
            AsignacionLimpieza o None: La entidad si existe, None en caso contrario
        """
        pass

    @abstractmethod
    def find_by_sala(self, sala_id: int) -> List[AsignacionLimpieza]:
        """
        Obtiene todas las asignaciones de limpieza para una sala específica.

        Args:
            sala_id: El ID de la sala

        Returns:
            List[AsignacionLimpieza]: Lista de asignaciones para la sala
        """
        pass

    @abstractmethod
    def find_by_limpiador(self, usuario_id: int) -> List[AsignacionLimpieza]:
        """
        Obtiene todas las asignaciones asignadas a un limpiador específico.

        Args:
            usuario_id: El ID del usuario limpiador

        Returns:
            List[AsignacionLimpieza]: Lista de asignaciones del limpiador
        """
        pass

    @abstractmethod
    def find_by_conserje(self, usuario_id: int) -> List[AsignacionLimpieza]:
        """
        Obtiene todas las asignaciones creadas por un conserje específico.

        Args:
            usuario_id: El ID del usuario conserje

        Returns:
            List[AsignacionLimpieza]: Lista de asignaciones creadas por el conserje
        """
        pass

    @abstractmethod
    def find_pendientes(self) -> List[AsignacionLimpieza]:
        """
        Obtiene todas las asignaciones pendientes.

        Returns:
            List[AsignacionLimpieza]: Lista de asignaciones pendientes
        """
        pass

    @abstractmethod
    def find_pendientes_por_edificio(self, edificio_id: int) -> List[AsignacionLimpieza]:
        """
        Obtiene asignaciones pendientes para un edificio específico.

        Args:
            edificio_id: El ID del edificio

        Returns:
            List[AsignacionLimpieza]: Lista de asignaciones pendientes del edificio
        """
        pass

    @abstractmethod
    def get_estadisticas_edificio(self, edificio_id: int) -> dict:
        """
        Obtiene estadísticas de asignaciones para un edificio.

        Args:
            edificio_id: El ID del edificio

        Returns:
            dict: Estadísticas como total asignaciones, completadas, pendientes,
                  tiempo promedio de completación, etc.
        """
        pass

    @abstractmethod
    def update(self, asignacion: AsignacionLimpieza) -> AsignacionLimpieza:
        """
        Actualiza una asignación existente.

        Args:
            asignacion: La entidad AsignacionLimpieza con los datos actualizados

        Returns:
            AsignacionLimpieza: La entidad actualizada

        Raises:
            ValueError: Si la asignación no existe
        """
        pass

    @abstractmethod
    def marcar_completada(self, asignacion_id: int) -> bool:
        """
        Marca una asignación como completada.

        Args:
            asignacion_id: El ID de la asignación

        Returns:
            bool: True si se marcó como completada

        Raises:
            ValueError: Si la asignación no existe o ya está completada
        """
        pass

    @abstractmethod
    def delete(self, asignacion_id: int) -> bool:
        """
        Elimina una asignación por su ID.

        Args:
            asignacion_id: El ID de la asignación a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        pass