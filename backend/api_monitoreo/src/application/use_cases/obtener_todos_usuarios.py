# src/application/use_cases/obtener_todos_usuarios.py
from src.domain.ports.usuario_repository import IUsuarioRepository

class ObtenerTodosUsuarios:
    """
    Caso de Uso: Obtener todos los usuarios.
    """

    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuario_repository = usuario_repository

    def ejecutar(self):
        """
        Obtiene todos los usuarios del sistema.

        Returns:
            list: Lista de entidades Usuario.
        """
        return self.usuario_repository.get_all()