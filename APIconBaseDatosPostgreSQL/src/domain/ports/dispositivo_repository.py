# src/domain/ports/dispositivo_repository.py
"""
Puerto (Interfaz) para el repositorio de dispositivos.
Define el contrato que deben implementar todos los adaptadores de persistencia de dispositivos.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.dispositivo import Dispositivo


class IDispositivoRepository(ABC):
    """
    Interfaz del repositorio de dispositivos.

    Define las operaciones de persistencia que cualquier adaptador
    de base de datos debe implementar para manejar dispositivos sensores.
    """

    @abstractmethod
    def save(self, dispositivo: Dispositivo) -> Dispositivo:
        """
        Guarda un nuevo dispositivo en la base de datos.

        Args:
            dispositivo: La entidad Dispositivo a persistir

        Returns:
            Dispositivo: La entidad con su ID asignado

        Raises:
            ValueError: Si ya existe un dispositivo con la misma MAC
        """
        pass

    @abstractmethod
    def find_by_id(self, dispositivo_id: int) -> Optional[Dispositivo]:
        """
        Busca un dispositivo por su ID.

        Args:
            dispositivo_id: El ID del dispositivo a buscar

        Returns:
            Dispositivo o None: La entidad Dispositivo si existe, None en caso contrario
        """
        pass

    @abstractmethod
    def find_by_mac(self, mac_address: str) -> Optional[Dispositivo]:
        """
        Busca un dispositivo por su dirección MAC.

        Args:
            mac_address: La dirección MAC del dispositivo

        Returns:
            Dispositivo o None: La entidad Dispositivo si existe, None en caso contrario
        """
        pass

    @abstractmethod
    def find_by_sala(self, sala_id: int) -> List[Dispositivo]:
        """
        Obtiene todos los dispositivos instalados en una sala específica.

        Args:
            sala_id: El ID de la sala

        Returns:
            List[Dispositivo]: Lista de dispositivos en la sala
        """
        pass

    @abstractmethod
    def find_by_universidad(self, universidad_id: int) -> List[Dispositivo]:
        """
        Obtiene todos los dispositivos de una universidad específica.

        Args:
            universidad_id: El ID de la universidad

        Returns:
            List[Dispositivo]: Lista de dispositivos de la universidad
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Dispositivo]:
        """
        Obtiene todos los dispositivos del sistema.

        Returns:
            List[Dispositivo]: Lista completa de dispositivos
        """
        pass

    @abstractmethod
    def get_conectados(self) -> List[Dispositivo]:
        """
        Obtiene todos los dispositivos que están conectados.

        Returns:
            List[Dispositivo]: Lista de dispositivos conectados
        """
        pass

    @abstractmethod
    def get_desconectados(self) -> List[Dispositivo]:
        """
        Obtiene todos los dispositivos que están desconectados.

        Returns:
            List[Dispositivo]: Lista de dispositivos desconectados
        """
        pass

    @abstractmethod
    def update(self, dispositivo: Dispositivo) -> Dispositivo:
        """
        Actualiza un dispositivo existente.

        Args:
            dispositivo: La entidad Dispositivo con los datos actualizados

        Returns:
            Dispositivo: La entidad actualizada

        Raises:
            ValueError: Si el dispositivo no existe
        """
        pass

    @abstractmethod
    def update_estado(self, dispositivo_id: int, estado: str) -> bool:
        """
        Actualiza solo el estado de un dispositivo.

        Args:
            dispositivo_id: El ID del dispositivo
            estado: El nuevo estado ('conectado' o 'desconectado')

        Returns:
            bool: True si se actualizó correctamente

        Raises:
            ValueError: Si el dispositivo no existe o el estado es inválido
        """
        pass

    @abstractmethod
    def delete(self, dispositivo_id: int) -> bool:
        """
        Elimina un dispositivo por su ID.

        Args:
            dispositivo_id: El ID del dispositivo a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no existía

        Raises:
            ValueError: Si no se puede eliminar (restricciones de integridad)
        """
        pass