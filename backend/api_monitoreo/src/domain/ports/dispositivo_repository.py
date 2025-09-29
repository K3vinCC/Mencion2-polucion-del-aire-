# src/domain/ports/dispositivo_repository.py
from abc import ABC, abstractmethod

class IDispositivoRepository(ABC):
    """
    Interfaz para el Repositorio de Dispositivos.
    """

    @abstractmethod
    def save(self, dispositivo):
        """Guarda un nuevo dispositivo en la base de datos."""
        pass

    @abstractmethod
    def find_by_id(self, dispositivo_id):
        """Busca un dispositivo por su ID."""
        pass

    @abstractmethod
    def find_by_token(self, token):
        """Busca un dispositivo por su token de acceso."""
        pass

    @abstractmethod
    def get_all(self):
        """Devuelve todos los dispositivos."""
        pass

    @abstractmethod
    def get_by_edificio(self, id_edificio):
        """Devuelve todos los dispositivos de un edificio."""
        pass

    @abstractmethod
    def update_ultima_lectura(self, dispositivo_id, timestamp):
        """Actualiza el timestamp de la última lectura de un dispositivo."""
        pass