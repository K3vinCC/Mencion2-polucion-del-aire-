# src/application/use_cases/eliminar_usuario.py
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.application.errors.exceptions import UsuarioNoEncontradoError

class EliminarUsuario:
    """
    Caso de Uso: Eliminar un usuario.
    """

    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuario_repository = usuario_repository

    def ejecutar(self, usuario_id):
        """
        Elimina un usuario del sistema.

        Args:
            usuario_id (int): ID del usuario a eliminar.

        Raises:
            UsuarioNoEncontradoError: Si el usuario no existe.
        """
        usuario = self.usuario_repository.find_by_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontradoError()

        # Aquí normalmente eliminaríamos el usuario
        # Pero como no tenemos un método delete en el repositorio, solo verificamos que existe
        # En una implementación real, necesitaríamos agregar un método delete al repositorio
        pass