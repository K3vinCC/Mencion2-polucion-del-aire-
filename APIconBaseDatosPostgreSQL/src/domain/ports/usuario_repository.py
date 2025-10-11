# src/domain/ports/usuario_repository.py
"""
Puerto (Interfaz) para el repositorio de usuarios.
Define el contrato que deben implementar todos los adaptadores de persistencia de usuarios.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.usuario import Usuario


class IUsuarioRepository(ABC):
    """
    Interfaz del repositorio de usuarios.

    Define las operaciones de persistencia que cualquier adaptador
    de base de datos debe implementar para manejar usuarios.
    """

    @abstractmethod
    def save(self, usuario: Usuario) -> Usuario:
        """
        Guarda un nuevo usuario en la base de datos.

        Args:
            usuario: La entidad Usuario a persistir

        Returns:
            Usuario: La entidad con su ID asignado

        Raises:
            ValueError: Si ya existe un usuario con el mismo email
        """
        pass

    @abstractmethod
    def find_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """
        Busca un usuario por su ID.

        Args:
            usuario_id: El ID del usuario a buscar

        Returns:
            Usuario o None: La entidad Usuario si existe, None en caso contrario
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Usuario]:
        """
        Busca un usuario por su email.

        Args:
            email: El email del usuario a buscar

        Returns:
            Usuario o None: La entidad Usuario si existe, None en caso contrario
        """
        pass

    @abstractmethod
    def find_by_universidad(self, universidad_id: int) -> List[Usuario]:
        """
        Obtiene todos los usuarios de una universidad específica.

        Args:
            universidad_id: El ID de la universidad

        Returns:
            List[Usuario]: Lista de usuarios de la universidad
        """
        pass

    @abstractmethod
    def find_by_rol(self, rol_id: int) -> List[Usuario]:
        """
        Obtiene todos los usuarios con un rol específico.

        Args:
            rol_id: El ID del rol

        Returns:
            List[Usuario]: Lista de usuarios con ese rol
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Usuario]:
        """
        Obtiene todos los usuarios del sistema.

        Returns:
            List[Usuario]: Lista completa de usuarios
        """
        pass

    @abstractmethod
    def update(self, usuario: Usuario) -> Usuario:
        """
        Actualiza un usuario existente.

        Args:
            usuario: La entidad Usuario con los datos actualizados

        Returns:
            Usuario: La entidad actualizada

        Raises:
            ValueError: Si el usuario no existe
        """
        pass

    @abstractmethod
    def delete(self, usuario_id: int) -> bool:
        """
        Elimina un usuario por su ID.

        Args:
            usuario_id: El ID del usuario a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no existía

        Raises:
            ValueError: Si no se puede eliminar (restricciones de integridad)
        """
        pass