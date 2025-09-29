# src/domain/ports/lectura_calidad_aire_repository.py
"""
Puerto (Interfaz) para el repositorio de lecturas de calidad del aire.
Define el contrato que deben implementar todos los adaptadores de persistencia.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from src.domain.entities.lectura_calidad_aire import LecturaCalidadAire


class ILecturaCalidadAireRepository(ABC):
    """
    Interfaz del repositorio de lecturas de calidad del aire.

    Define las operaciones de persistencia que cualquier adaptador
    de base de datos debe implementar para manejar lecturas de PM.
    """

    @abstractmethod
    def save(self, lectura: LecturaCalidadAire) -> LecturaCalidadAire:
        """
        Guarda una nueva lectura de calidad del aire.

        Args:
            lectura: La entidad LecturaCalidadAire a persistir

        Returns:
            LecturaCalidadAire: La entidad con su ID asignado
        """
        pass

    @abstractmethod
    def find_by_id(self, lectura_id: int) -> Optional[LecturaCalidadAire]:
        """
        Busca una lectura por su ID.

        Args:
            lectura_id: El ID de la lectura a buscar

        Returns:
            LecturaCalidadAire o None: La entidad si existe, None en caso contrario
        """
        pass

    @abstractmethod
    def find_by_dispositivo(self, dispositivo_id: int, limit: int = 100) -> List[LecturaCalidadAire]:
        """
        Obtiene las últimas lecturas de un dispositivo específico.

        Args:
            dispositivo_id: El ID del dispositivo
            limit: Número máximo de lecturas a retornar (más recientes primero)

        Returns:
            List[LecturaCalidadAire]: Lista de lecturas ordenadas por fecha descendente
        """
        pass

    @abstractmethod
    def find_by_sala(self, sala_id: int, limit: int = 100) -> List[LecturaCalidadAire]:
        """
        Obtiene las últimas lecturas de todos los dispositivos en una sala.

        Args:
            sala_id: El ID de la sala
            limit: Número máximo de lecturas por dispositivo

        Returns:
            List[LecturaCalidadAire]: Lista de lecturas de todos los dispositivos de la sala
        """
        pass

    @abstractmethod
    def find_by_rango_fechas(
        self,
        dispositivo_id: int,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> List[LecturaCalidadAire]:
        """
        Obtiene lecturas de un dispositivo en un rango de fechas.

        Args:
            dispositivo_id: El ID del dispositivo
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango

        Returns:
            List[LecturaCalidadAire]: Lista de lecturas en el rango especificado
        """
        pass

    @abstractmethod
    def get_ultima_lectura(self, dispositivo_id: int) -> Optional[LecturaCalidadAire]:
        """
        Obtiene la última lectura de un dispositivo.

        Args:
            dispositivo_id: El ID del dispositivo

        Returns:
            LecturaCalidadAire o None: La última lectura o None si no hay lecturas
        """
        pass

    @abstractmethod
    def get_lecturas_problematicas(self, horas: int = 24) -> List[LecturaCalidadAire]:
        """
        Obtiene lecturas que indican problemas de calidad del aire en las últimas horas.

        Args:
            horas: Número de horas hacia atrás para buscar

        Returns:
            List[LecturaCalidadAire]: Lista de lecturas con calidad deficiente
        """
        pass

    @abstractmethod
    def get_promedio_calidad_aire(
        self,
        dispositivo_id: int,
        horas: int = 24
    ) -> Optional[dict]:
        """
        Calcula el promedio de calidad del aire de un dispositivo en las últimas horas.

        Args:
            dispositivo_id: El ID del dispositivo
            horas: Número de horas para el cálculo

        Returns:
            dict o None: Diccionario con promedios de PM1, PM2.5, PM10 y nivel de calidad
        """
        pass

    @abstractmethod
    def delete_antiguas(self, dias: int = 90) -> int:
        """
        Elimina lecturas anteriores a un número de días especificado.

        Args:
            dias: Número de días de antigüedad para eliminar

        Returns:
            int: Número de lecturas eliminadas
        """
        pass