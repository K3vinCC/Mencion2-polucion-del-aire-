from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.usuario import Usuario

class IUsuarioRepository(ABC):
    """Interfaz para el repositorio de usuarios"""
    
    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario:
        """Crea un nuevo usuario"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por su email"""
        pass
    
    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario existente"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un usuario por su ID"""
        pass
    
    @abstractmethod
    def listar_por_universidad(self, universidad_id: int) -> List[Usuario]:
        """Lista todos los usuarios de una universidad"""
        pass