# src/domain/ports/usuario_repository.py
from abc import ABC, abstractmethod

class IUsuarioRepository(ABC):
    """
    Interfaz (Puerto) para el Repositorio de Usuarios.

    Define un contrato de los métodos que cualquier adaptador de persistencia.
    debe implementar para manejar los datos de los usuarios.

    Esto cumple con el Principio de Inversión de Dependencias (la 'D' de SOLID),
    ya que las capas superiores de la aplicación dependerán de esta abstracción,
    no de una implementación concreta.
    """

    @abstractmethod
    def save(self, usuario):
        """Guarda un nuevo usuario en la base de datos."""
        pass

    @abstractmethod
    def find_by_email(self, correo):
        """Busca un usuario por su correo electrónico."""
        pass

    @abstractmethod
    def find_by_id(self, usuario_id):
        """Busca un usuario por su ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Devuelve todos los usuarios."""
        pass